import requests
name = 'ScuffedAPI'

Scuffed_API = 'http://scuffedapi.xyz/api/'

# Get any cosmetic, not checking cosmetic type.

def getPlaylist(search):
    url = Scuffed_API + 'api/playlists?search=' + search
    apir = requests.get(url).json()
    return apir
