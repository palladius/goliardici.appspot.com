from google.appengine.ext import db, ndb
from google.appengine.api.users import User
import wtforms
from wtforms.compat import text_type, string_types
import operator
import warnings
import widgets


class UserField(wtforms.Field):
    """
    A field that alls WTForms to produce a field that can be used
    to edit a db.UserProperty or ndb.UserProperty. Displays as a text field with an
    Email.
    """
    widget = wtforms.widgets.TextInput()
    __temporary_data = None

    def _value(self):
        if self.data:
            return self.data.email()
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = User(valuelist[0])
        else:
            self.data = None

    def pre_validate(self, form):
        if self.data:
            self.__temporary_data = self.data
            self.data = self.data.email()

    def post_validate(self, form, validation_stopped):
        if self.__temporary_data:
            self.data = self.__temporary_data


def convert_UserProperty(model, prop, kwargs):
    """Returns a form field for a ``db.UserProperty``."""
    if isinstance(prop, db.Property) and (prop.auto_current_user or prop.auto_current_user_add):
        return None
    elif isinstance(prop, ndb.Property) and (prop._auto_current_user or prop._auto_current_user_add):
        return None

    kwargs['validators'].append(wtforms.validators.email())
    kwargs['validators'].append(wtforms.validators.length(max=500))
    return UserField(**kwargs)


class KeyPropertyField(wtforms.fields.SelectFieldBase):
    """
    Identical to the non-ndb counterpart, but only supports ndb references.
    """
    widget = wtforms.widgets.Select()

    def __init__(self, label=None, validators=None, kind=None,
                 label_attr=None, get_label=None, allow_blank=False,
                 blank_text='', **kwargs):
        super(KeyPropertyField, self).__init__(label, validators,
                                                     **kwargs)
        if label_attr is not None:
            warnings.warn('label_attr= will be removed in WTForms 1.1, use get_label= instead.', DeprecationWarning)
            self.get_label = operator.attrgetter(label_attr)
        elif get_label is None:
            self.get_label = lambda x: x
        elif isinstance(get_label, string_types):
            self.get_label = operator.attrgetter(get_label)
        else:
            self.get_label = get_label

        self.allow_blank = allow_blank
        self.blank_text = blank_text
        self._set_data(None)
        if kind is not None:
            if isinstance(kind, basestring):
                kind = ndb.Model._kind_map[kind]
            self.query = kind.query()
        else:
            self.query = None

    def _value(self):
        if self.data:
            return self.data.urlsafe()
        else:
            return '__None'

    def _get_data(self):
        if self._formdata is not None:
            if self.query:
                for obj in self.query:
                    if obj.key.urlsafe() == self._formdata:
                        self._set_data(obj.key)
                        break
            else:
                self._set_data(ndb.Key(urlsafe=self._formdata))
        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def iter_choices(self):
        if self.allow_blank or not self.query:
            yield ('__None', self.blank_text, self.data is None)

        if self.query:
            for obj in self.query:
                key = obj.key.urlsafe()
                label = self.get_label(obj)
                yield (key, label, self.data and (self.data == obj.key))
        elif self.data:
            yield(key, self.get_label(key.get()), True)

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = None
            else:
                self._data = None
                self._formdata = valuelist[0]

    def pre_validate(self, form):
        if not self.allow_blank or self.data is not None and self.query:
            for obj in self.query:
                if self.data.urlsafe() == obj.key.urlsafe():
                    break
            else:
                raise ValueError(self.gettext('Not a valid choice'))


class MultipleReferenceField(wtforms.SelectMultipleField):
    """
    Allows WTForms to display a field for a db.List(db.Key),
    db.MultipleReferenceProperty, or ndb.KeyProperty(repeated=True). Shows the options as a list of
    checkboxes. The referenced class must have a __str__ or __unicode__
    method defined.
    """
    widget = widgets.MultipleReferenceCheckboxWidget()
    option_widget = wtforms.widgets.CheckboxInput()

    def __init__(self, kind, choices=None, validate_choices=True, *args, **kwargs):
        super(MultipleReferenceField, self).__init__(*args, **kwargs)
        if isinstance(kind, basestring):
                kind = ndb.Model._kind_map[kind]
        self.kind = kind
        if choices is None:
            if kind:
                if issubclass(kind, ndb.Model):
                    choices = [(x.key, x.name) for x in kind.query()]
                else:
                    choices = [(x.key(), x.name) for x in kind.all()]
            else:
                choices = []
        elif not choices:
            choices = []
        self.choices = choices
        self.validate_choices = validate_choices

    def iter_choices(self):
        for value, label in self.choices:
            selected = self.data is not None and value in self.data

            if not self.kind or issubclass(self.kind, ndb.Model):
                value = value.urlsafe()

            yield (value, label, selected)

    def pre_validate(self, form):
        if self.validate_choices:
            super(MultipleReferenceField, self).pre_validate(form)

    def process_data(self, value):
        try:
            self.data = list(v for v in value)
        except (ValueError, TypeError):
            self.data = []

    def process_formdata(self, valuelist):
        if valuelist:
            if not self.kind or issubclass(self.kind, ndb.Model):
                self.data = [ndb.Key(urlsafe=x) for x in valuelist]
            else:
                self.data = [db.Key(x) for x in valuelist]
        else:
            self.data = []
