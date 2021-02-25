from urllib.parse import urlencode

class apiUrls:
    def __init__(self):
        self.base = 'https://ch.tetr.io/api' # base api url

        self.stats = f'{self.base}/general/stats'
        self.activity = f'{self.base}/general/activity'
        self.user = f'{self.base}/users'
        self.tetraLeague = f'{self.base}/users/lists/league'
        self.fulltetraLeague = f'{self.tetraLeague}/all'
        self.xp = f'{self.base}/users/lists/xp'
        self.stream = f'{self.base}/streams'
        self.news = f'{self.base}/news'
    
    def recordUrl(self, user):
        return self.addParam(self.user, user) + '/records'

    def addParam(self, url, param):
        url += f'/{param}'
        return url
    
    def addQureyParam(self, url, params):
        url += f'?{urlencode(params)}'
        return url