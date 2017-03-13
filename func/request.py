# Carries out requests to Trello API. Also parses GET requests.

import requests
import json

f = open('config.txt', 'r')

API_URL         = 'https://api.trello.com/'
API_KEY         = f.readline().strip('\n')
TOKEN           = f.readline()
REQUEST_POSTFIX = '?key=' + API_KEY + '&token=' + TOKEN


def get(url, params=''):
    """Returns a dict containing the contents of the GET response"""
    content = requests.get(API_URL + url + REQUEST_POSTFIX, params).content.decode("utf-8")
    return json.loads(content)
