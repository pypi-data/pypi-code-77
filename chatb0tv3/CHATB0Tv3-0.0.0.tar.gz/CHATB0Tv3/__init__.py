import requests
import json

class Chatbot:
    def __init__(self, res):
        self.res = res

    def response(self):
        response1 = requests.get(
            "https://really-epic-api.thisguy3.repl.co/api/chatbot/{}".format(self.res)).text
        response1 = json.loads(response1)
        response1 = response1.get("Response")
        return response1