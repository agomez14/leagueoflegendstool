#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, jinja2, os, logging, urllib2, urllib, json

from google.appengine.api import urlfetch
from settings import *

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader("html"))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(template_values))

class SumdIdHandler(webapp2.RequestHandler):
    def get(self):
        summoner_name = str(self.request.get('summoner')).lower()
        region = self.request.get('region').lower()
        
        # Summoner Name to Summoner ID
        sum_url = "https://na.api.pvp.net/api/lol/"+region+"/v1.4/summoner/by-name/"+summoner_name+"?api_key="+RIOT_API_KEY
        response = urlfetch.fetch(url=sum_url)
        sum_data = json.loads(response.content)

        #SummonerID to MatchHistory
        sum_id = str(sum_data[summoner_name]['id'])
        hist_url = "https://na.api.pvp.net/api/lol/"+region+"/v2.2/matchhistory/"+sum_id+"?api_key="+RIOT_API_KEY
        response = urlfetch.fetch(url=hist_url)
        hist_data = json.loads(response.content)
        
        template_values = {}
        for x in range(0,len(hist_data['matches'])):
            template_values[x] = hist_data['matches'][x]
        template = jinja_environment.get_template('history.html')
        self.response.out.write(template.render(template_values=template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sumid', SumdIdHandler)
], debug=True)
