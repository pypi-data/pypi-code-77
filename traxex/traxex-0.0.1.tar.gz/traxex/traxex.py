import urllib

from . import http, dict, errors

noresponse = "eyy sorry im just a dog.."

def ongoing():
    try:
        return http.get("/ongo.php")["data"]
    except Exception as e:
        raise errors.NothingFound(noresponse)


def upcoming():
    try:
        return http.get("/up.php")["data"]
    except Exception as e:
        raise errors.NothingFound(noresponse)


def ended():
    try:
        return http.get("/comp.php")["data"]
    except Exception as e:
        raise errors.NothingFound(noresponse)
