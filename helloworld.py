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

import simplejson
import logging
import datetime
import urllib

import copy
class RingBuffer:
    def __init__(self,size):
        self.buffer = [[0 for i in range(2)] for j in range(size)]
        self.start = 0
        self.end = 0
        logging.info('NNNNNNNNNNNNNNNNew')

    def add(self,date,val):
        logging.info('add start')
        self.buffer[self.end][0] = date
        self.buffer[self.end][1] = val
        self.end = (self.end + 1) % len(self.buffer)
        logging.info('add end')
    def get(self):
         logging.info('get start')
         l = copy.deepcopy(self.buffer)
         l.sort()
         while [0,0] in l: l.remove([0,0])
         logging.info('get end')
         return l
#        val = self.buffer[self.start]
#        self.start =(self.start + 1) % len(self.buffer)
#        return val

    def __len__(self):
        return self.end - self.start

ring = RingBuffer(400)

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

        global ring
        
        content = self.request.get('json')
        jsonObj = simplejson.loads(content)

        date = datetime.datetime.utcfromtimestamp(jsonObj["date"])

        ring.add(int(time.mktime(date.timetuple()))*1000,jsonObj["value"])
        logging.info('Post')
#        self.redirect('/')

class Getjson(webapp.RequestHandler):
    def get(self):
        global ring

        contstr = str(ring.get())
        logging.info('ring = %s' % contstr)
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
