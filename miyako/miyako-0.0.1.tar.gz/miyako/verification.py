import requests, sys

class miyako:
    def verify(key):
        r = requests.post('https://keyauth.com/api/v4/',data={"type":"login","key":key,"name":"miyako","ownerid":"oOS357bVES"})
        if key in r.text:
        	pass
        else:
        	sys.exit()
