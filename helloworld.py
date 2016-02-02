import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import os
from google.appengine.ext.webapp import template

import datetime
import locale
import time

import json
import logging
import datetime
import urllib

from collections import deque
#import copy
que = deque([],400)

class Greeting(db.Model):

    value = db.FloatProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        d = datetime.datetime.today()

#        greetings_query = Greeting.all().order('-date')
#        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
#            'greetings': greetings,
#            'url': url,
#            'url_linktext': url_linktext,
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
    def post(self):

        content = self.request.get('json')
        jsonObj = json.loads(content)

        date = datetime.datetime.utcfromtimestamp(jsonObj["date"])

	que.append([int(time.mktime(date.timetuple()))*1000,jsonObj["value"]])
        logging.info('Post')
#        self.redirect('/')

class Getjson(webapp.RequestHandler):
    def get(self):

        contstr = str(list(que))
        logging.info('que = %s' % contstr)
        dst = contstr.replace('L', '')
        self.response.out.write(dst)
#"""





application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
                                      ('/getjson', Getjson)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
