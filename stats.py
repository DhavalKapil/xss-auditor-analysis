import alexa
from bs4 import BeautifulSoup
import requests
import requests_cache
import json

# Using cache
requests_cache.install_cache('cache')

JS_STATS_FILE = 'js_stats.json'
X_XSS_STATS_FILE = 'x_xss_stats.json'
RANK_FILE = 'rank.json'
EXTERNAL_JAVASCRIPTS = [
  'jquery',
  'react',
  'bootstrap',
  'angular',
  'moment',
  'socket.io',
  'ember',
  'backbone',
  'reveal',
  'underscore',
  'lodash',
  'mocha',
  'meteor',
  'mercury',
  'dojo',
  'ext-core',
  'hammer',
  'mootools',
  'prototype',
  'scriptaculous',
  'swfobject',
  'three',
  'webfont'
]

def parse_websites(websites):
  js_stats = {}
  x_xss_stats = {}

  for website in websites:
    print(website[1])
    try:
      response = requests.get('http://' + website[1])
      soup = BeautifulSoup(response.text, 'lxml')

      # Extracting script file sources
      for script in soup.find_all('script'):
        source = script.get('src')
        # Skipping inline scripts
        if source != None:
          # Considering scripts from different domain
          if (website[1].split('.')[0] not in source) and (source.startswith('http') or source.startswith('//')):
            for javascript in EXTERNAL_JAVASCRIPTS:
              if javascript in source:
                if website[1] not in js_stats:
                  js_stats[website[1]] = []
                js_stats[website[1]].append({'js': javascript, 'srd': source})

      # Checking X-XSS-Protection header
      xss_header = 'default'
      # Lower casing all header keys
      headers = {k.lower():v for k,v in response.headers.items()}
      if 'x-xss-protection' in headers:
        xss_header = headers['x-xss-protection']
      x_xss_stats[website[1]] = xss_header

    except Exception as error:
      print(error)
      continue
  return js_stats, x_xss_stats

websites = alexa.top_list(500)
js_stats, x_xss_stats = parse_websites(websites)
with open(JS_STATS_FILE, 'w') as outfile:
  json.dump(js_stats, outfile)
with open(X_XSS_STATS_FILE, 'w') as outfile:
  json.dump(x_xss_stats, outfile)
with open(RANK_FILE, 'w') as outfile:
  json.dump(websites, outfile)
