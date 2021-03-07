import urllib3
import json
from ..db import db

DEFINE_URL = 'https://osutrack-api.ameo.dev/'

#TODO: get new highscores

# osutrack API request to update and fetch changes since last update
def updateUser(uid : int):
    url = f'{DEFINE_URL}update?user={uid}&mode=0'
    http = urllib3.PoolManager()
    request = http.request('POST', url)
    return json.loads(request.data)


# osutrack API request to get rank and acc from user
def getUserPeak(uid : int):
    url = f'{DEFINE_URL}peak?user={uid}&mode=0'
    http = urllib3.PoolManager()
    request = http.request('GET', url)
    return json.loads(request.data)[0]


def registerOsuID(member_id : int, uid : int):
    db.execute("UPDATE osu SET osu_id = ? WHERE member_id = ?;", uid, member_id)
    db.commit()


def fetchOsuID(member_id : int):
    uid = db.field("SELECT osu_id FROM osu WHERE member_id = ?;", member_id)
    return uid
