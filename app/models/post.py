from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb


class Post(BasicModel):
    title = ndb.StringProperty()
    content = ndb.TextProperty()

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