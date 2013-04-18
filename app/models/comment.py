from ferris.core.ndb import BasicModel
from google.appengine.ext import ndb

'''
This is a comment to a post. Test to reference



HISTORY:
 - 1.00 removed 'user', default 

'''

MODEL_VERSION = '1.00'

#from post import Post

class Comment(BasicModel):
    #user    = ndb.StringProperty() # intrinsic from
    content = ndb.TextProperty()
    #post_id = ndb.KeyProperty(kind=Post)
    post_ref= ndb.KeyProperty(kind='Post', required=True)
    model_version = ndb.StringProperty(default = MODEL_VERSION)

