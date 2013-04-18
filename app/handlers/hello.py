from ferris.core.handler import Handler
from ferris.core.handler import Handler, route

class Hello(Handler):

    def list2(self):
        return "Hello, is it me you're looking for?"

    def list(self):
      #self.set(who=self.request.params['name'] or self.request.params )
      #keys = [ el for el in self.request.params ]
      keys = self.request.params
      if 'name' in keys:
        self.set(who=self.request.params['name'])
      else:
        self.set(who="Missing 'name' key in: {}".format(keys))

    @route
    def custom2(self):
      return "Something, indeed."

    @route
    def custom(self, text):
      return "%s, indeed." % text

    @route
    def add(self):
      return "This is not Rails, my friend :)"
