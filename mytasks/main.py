from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write("Hello App Engine!")

application = webapp.WSGIApplication([('/', MainHandler)], debug=True)


def main():
  run_wsgi_app(application)