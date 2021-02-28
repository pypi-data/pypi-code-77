import komiker as _k

class extra:
	
	def __init__(self):
		self.path = _k._o.dirname(__file__)
		
	def read(self):
		bo = open(f'{self.path}/data.json').read()
		bp = ''.join(([chr(k) for k in range(65, 91)])[x]+([chr(j) for j in range(97, 123)])[x] for x in range(26))
		bq = _k._j(_k._b(''.join((lambda c: (bp[26:]+bp[:26])[bp.find(c)] if bp.find(c) != -1 else c)(c) for c in bo)).decode('utf8'))
		return bq
		
	def print(self, a=None, b=True):
		h=chr(72)*2
		w=_k._up(h, _k._fi(0, _k._tz, _k._pc(h, 0, 0)))[1]
		if a != None and a != False:
			if b:
				ltx = len(a)
				s=(w-ltx)//2
				p=(s*2)+ltx-(w-8)
				x=p//2
				y=p-x
				r='─' * (s-x)
				l='─' * (s-y)
				print(f'\33[32m\33[1m{l}\33[0m\33[1m\40\40\u300a{a}\40\u300b\40\33[0m\33[32m\33[1m{r}\33[0m')
			else:
				t = a.splitlines()
				print('\33[97m\33[1m%s\n'%t[0])
				for e in _k._tw(t[1], w-1): print(e)
				print('\33[0m')
		elif a == False: print('\33[32m\33[1m%s\33[0m' % '─' * w)
		else: print()
			
	def err(self, string, b=True):
		print(f'\33[32m\nError:\40{string}\33[0m')
		if b: exit()