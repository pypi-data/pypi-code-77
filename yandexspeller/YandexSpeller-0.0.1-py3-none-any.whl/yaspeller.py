import requests

__all__ = ['check']


class Result:
	'''Spell checker result'''
	
	def __init__(self, is_ok, matches):
		self.is_ok = is_ok
		self.matches = matches
	
	def __bool__(self):
		return self.is_ok
	
	def first_match(self):
		'''First match for result'''
		if len(self.matches) > 0:
			return self.matches[0]
		return None


def check(word, lang='en'):
	'''Spell check'''
	if word.strip() == '':
		raise ValueError('expected a word')
	if lang not in ['en', 'ru']:
		raise ValueError('language must be "ru" or "en"')
	params = {'text': word, 'lang': lang}
	r = requests.get('http://speller.yandex.net/services/spellservice.json/checkText', params=params)
	if len(r.json()) > 0:
		return Result(False, [v for v in r.json()[0]['s']])
	else:
		return Result(True, [])