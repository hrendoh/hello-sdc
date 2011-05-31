from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from xml.etree.ElementTree import *

user = users.get_current_user()
class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      url = 'http://localhost/news.feed'
      #url = 'http://localhost/news.php'
      result = urlfetch.fetch(url,
                        headers={'use_intranet': 'yes'})
      self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
      if result.status_code == 200:
        rss = fromstring(result.content)
        for item in rss.getiterator('item'):
          title = item.find('title')
          link = item.find('link')
          self.response.out.write('<a href=' + link.text + '>'+ title.text + '</a><br>')
    else:
      self.redirect(users.create_login_url(self.request.uri))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
