# libs
import requests
import json

# code
# getPrioq data
def getPrioq(whatDo):
    if whatDo == "queue":
        # vars
        url = "https://api.2b2t.dev/prioq"
        htmlContent = requests.get(url)
        jsonDumped = json.dumps(htmlContent.text)
        jsonLoaded = json.loads(jsonDumped)
        # get prioq var operation
        prioqRslt = ""
        prioqIndex = jsonLoaded.index(",")
        prioqIndex = prioqIndex + 1
        prioqRslt = jsonLoaded[prioqIndex:]
        prioqIndex = prioqRslt.index(",")
        prioqRslt = prioqRslt[:prioqIndex]
        # return result
        return prioqRslt
    if whatDo == "time":
        # vars
        url = "https://api.2b2t.dev/prioq"
        htmlContent = requests.get(url)
        jsonDumped = json.dumps(htmlContent.text)
        jsonLoaded = json.loads(jsonDumped)
        # get prioq var operation
        prioqIndex = jsonLoaded.index("\"")
        prioqIndex = prioqIndex + 1
        prioqRslt = jsonLoaded[prioqIndex:]
        prioqIndex = prioqRslt.index("\"")
        prioqRslt = prioqRslt[:prioqIndex]
        return prioqRslt

# seenPlayer data
def seenPlayer(username):
    # vars
    url = "https://api.2b2t.dev/seen?username=" + username
    htmlContent = requests.get(url)
    jsonDumped = json.dumps(htmlContent.text)
    jsonLoaded = json.loads(jsonDumped)
    # get seen var operation
    seenIndex = jsonLoaded.index(":")
    seenIndex = seenIndex + 2
    seenResult = jsonLoaded[seenIndex:]
    seenIndex = seenResult.index("\"")
    seenResult = seenResult[:seenIndex]
    print(seenResult)

# playerStats data
def getPlayerStats(username, whatDo):
    # vars
    url = "https://api.2b2t.dev/stats?username=" + username
    htmlContent = requests.get(url)
    jsonDumped = json.dumps(htmlContent.text)
    jsonLoaded = json.loads(jsonDumped)
    # getId
    if whatDo == "id":
        statsIndex = jsonLoaded.index("id")
        statsIndex = statsIndex + 4
        statsRslt = jsonLoaded[statsIndex:]
        statsIndex = statsRslt.index(",")
        statsRslt = statsRslt[:statsIndex]
        return statsRslt
    # getUUID
    if whatDo == "uuid":
        statsIndex = jsonLoaded.index("uuid")
        statsIndex = statsIndex + 7
        statsRslt = jsonLoaded[statsIndex:]
        statsIndex = statsRslt.index("kills")
        statsIndex = statsIndex - 8
        statsRslt = statsRslt[:statsIndex]
        return statsRslt
    # getKills
    if whatDo == "kills":
        statsIndex = jsonLoaded.index("kills")
        statsIndex = statsIndex + 7
        statsRslt = jsonLoaded[statsIndex:]
        statsIndex = statsRslt.index("deaths")
        statsIndex = statsIndex - 2
        statsRslt = statsRslt[:statsIndex]
        return statsRslt
    # getJoins
    if whatDo == "joins":
        statsIndex = jsonLoaded.index("joins")
        statsIndex = statsIndex + 7
        statsRslt = jsonLoaded[statsIndex:]
        statsIndex = statsRslt.index("leaves")
        statsIndex = statsIndex - 2
        statsRslt = statsRslt[:statsIndex]
        return statsRslt
    # getLeaves
    if whatDo == "leaves":
        statsIndex = jsonLoaded.index("leaves")
        statsIndex = statsIndex + 8
        statsRslt = jsonLoaded[statsIndex:]
        statsIndex = statsRslt.index("adminlevel")
        statsIndex = statsIndex - 2
        statsRslt = statsRslt[:statsIndex]
        return statsRslt    