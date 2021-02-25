import requests
import dateutil.parser
from .urls import apiUrls
from .records import getRecords
from .base import Base

urls = apiUrls()

class User(Base):
    def __init__(self, data):
        self.ts = None
        super().__init__(data)
        self.league = LeagueData(data['league'])
        if self.ts:
            self.createdat = dateutil.parser.parse(self.ts)
        else:
            self.createdat = 'not tracked'
    
    def getAvatar(self):
        return f'https://tetr.io/user-content/avatars/{self.id}.jpg'
    
    def emojiFlag(self):
        out = ''
        if not self.country:
            return None
        letters = '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿'
        for letter in self.country:
            out +=letters[ord(letter) - 65]
        return out
    
    def getRecords(self):
        return getRecords(self.username)

class LeagueData(Base):
    def __init__(self, data):
        super().__init__(data)

    def getRankImage(self):
        return f'https://tetr.io/res/league-ranks/{self.rank}.png'

def getUser(name):
    url = urls.user
    url = urls.addParam(url, name)
    with requests.Session() as ses:
        resp = ses.get(url).json()
        if not resp['success']:
            raise Exception(resp['error'])
    json = resp['data']['user']
    return User(json)