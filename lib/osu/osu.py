import urllib3
import json

DEFINE_URL = 'https://osutrack-api.ameo.dev/'

#TODO: get new highscores

def updateUser(uid):
    url = f'{DEFINE_URL}update?user={uid}&mode=0'
    http = urllib3.PoolManager()
    request = http.request('POST', url)
    return json.loads(request.data)


def getUserPeak(uid):
    url = f'{DEFINE_URL}peak?user={uid}&mode=0'
    http = urllib3.PoolManager()
    request = http.request('GET', url)
    return json.loads(request.data)[0]
