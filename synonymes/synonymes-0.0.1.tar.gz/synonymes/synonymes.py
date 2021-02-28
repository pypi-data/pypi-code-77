import requests
from bs4 import BeautifulSoup
import re
import unidecode

def synonymo(mot):
    r = requests.get(f"http://www.synonymo.fr/synonyme/{mot}")
    r.encoding = r.apparent_encoding
    bs = BeautifulSoup(r.text, 'html.parser')
    words = bs.find_all('a', {'class': 'word', 'title': re.compile('.+')})
    if words == None:
        return ()
    for word in words:
        yield word.text.strip()

def linternaute(mot):
    # retirer les accents
    mot = unidecode.unidecode(mot)
    r = requests.get(f"https://www.linternaute.fr/dictionnaire/fr/synonyme/{mot}")
    r.encoding = r.apparent_encoding
    bs = BeautifulSoup(r.text, 'html.parser')
    words = bs.find('ul', {'class': 'dico_liste grid_line'})
    if words == None:
        return ()
    words = words.findChildren('a')
    for word in words:
        yield word.text.strip()

def larousse(mot):
    # retirer les accents
    mot = unidecode.unidecode(mot)
    r = requests.get(f"https://www.larousse.fr/dictionnaires/francais/{mot}/#synonyme", allow_redirects=True)
    r.encoding = r.apparent_encoding
    bs = BeautifulSoup(r.text, 'html.parser')
    synonyms_headers = bs.find_all('p', string='Synonymes :')
    if synonyms_headers == None:
        return ()
    for header in synonyms_headers:
       for word in header.find_next('li').text.split('-'):
            yield word.strip()

def cnrtl(mot):
    r = requests.get(f"https://www.cnrtl.fr/synonymie/{mot}")
    r.encoding = r.apparent_encoding
    bs = BeautifulSoup(r.text, 'html.parser')
    words = bs.find_all('td', {'class': 'syno_format'})
    if words == None:
        return ()
    for word in words:
        yield word.findChildren('a')[0].text.strip()
