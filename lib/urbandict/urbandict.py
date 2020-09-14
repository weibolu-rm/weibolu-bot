import urllib.request
import urllib.parse
import json

DEFINE_URL = 'https://api.urbandictionary.com/v0/define?term='

class UrbanDict():
    def __init__(self, term, definition, example, link):
        self.term = term
        self.definition = definition
        self.example = example
        self.link = link

    def __str__(self):
        return f"""
**{self.term}:**
*{self.definition}* 
>>> {self.example}
"""

def getDefinitionsJson(url):
    f = urllib.request.urlopen(url)
    data = json.loads(f.read().decode('utf-8'))
    f.close()
    return data

def parseDefinitionsJson(json):
    res = []

    if json is None:
        print('error parsing UD')
        return
    else:
        for definition in json['list']:
            ud = UrbanDict(
                definition['word'],
                definition['definition'],
                definition['example'],
                definition['permalink'] )
            res.append(ud)
        return res

def define(term):
    json = getDefinitionsJson(DEFINE_URL + urllib.parse.quote(term))
    return parseDefinitionsJson(json)
        