
from ferris.core.easy_handler import EasyHandler, scaffold

@scaffold
class Posts(EasyHandler):
    
	@scaffold
	def edit(self, id):
		pass
      #post = self.key_from_string(id).get()
      #if post.created_by != self.user:
      #  return 401
      #return self.scaffold.edit(self, id)

