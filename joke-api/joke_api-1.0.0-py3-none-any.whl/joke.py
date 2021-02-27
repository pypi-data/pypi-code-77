import requests
import json

def random_10():
    data = requests.get("https://official-joke-api.appspot.com/random_ten")
    tt = json.loads(data.text)
    l = []
    for item in (tt):
        l += [
            {
                "type": item["type"],
                "question": item["setup"],
                "answer": item["punchline"]
            }
        ]
    return l

def random():
    data = requests.get("https://official-joke-api.appspot.com/random_joke")
    tt = json.loads(data.text)
    d = {}
    for item in (tt):
       d.update(type=item["type"], question=item["setup"], answer=item["punchline"])

    return d 