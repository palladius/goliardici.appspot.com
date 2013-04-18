from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb

# 1.0.1 Added url and model_version

class Post(BasicModel):
    title         = ndb.StringProperty()
    content       = ndb.TextProperty()
    url           = ndb.TextProperty()
    model_version = ndb.TextProperty(default='1.0.1')  # should be hidden

    @classmethod
    def all_posts(cls):
        """
        Queries all posts in the system, regardless of user, ordered by date created descending.
        """
        return cls.query().order(-cls.created)

    @classmethod
    def all_posts_by_user(cls, user=None):
        """
        Queries all posts in the system for a particular user, ordered by date created desceding.
        If no user is provided, it returns the posts for the current user.
        """
        if not user:
            user = users.get_current_user()
        return cls.find_all_by_created_by(user).order(-cls.created)