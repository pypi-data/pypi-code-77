import komiker as _k

dó, án, von = '',[],''	# íslenska

class lib:
	
	def __init__(self, *args):
		
		self.alias = args[0]
		self.ex = _k._ex()
		self.path = self.ex.path
		self.regex = self.ex.read()
		self.dict = self.regex.get(self.alias)
		self.web = self.dict[3]
		self.ver = self.update()
		self.dir = '/storage/emulated/0/Download/Manga'
		
	def initData(self):
		v = open(f'{self.path}/data/{self.alias}.json')
		y = 0
		global dó, án
		án = [{_k._u(i[0]):i[1]} for i in _k._c(r'\"(.*?) => (.*?)\"').findall(v.read())]
		v.close()
		for j in án:
			y +=1 			
			for x in j.keys(): dó += f'\33[32mid:{str(y).zfill(len(str(len(án))))} -- ※ {x}\n\33[0m'		
		self.ex.print(f'daftar manga {self.web}'.title())
		print('\n%s' % dó)
		self.ex.print(False)
		idn = input('🥀 Masukan id manga: ')
		if idn.isnumeric(): idi = int(idn)
		else: self.ex.err('Masukan angka saja!')
		if idi > 0 and idi <= len(án):
			title = list(án[idi-1].keys())[0]	
			uid = list(án[idi-1].values())[0]
			dó, án = '', []
			return title, uid
		else: self.ex.err('Masukan id manga dengan benar!')
	
	async def request(self, a, b):
		async with _k._cs() as ss:
			if b == None:
				async with ss.get(a, ssl=False, headers=self.ref('https://'+self.web)) as r: return await r.read(), r.status
			else: 
				async with ss.post(a, data=b[0], ssl=False, headers=self.ref(b[1])) as r: return await r.read(), r.status
				
	def contentWeb(self, a, b=False, c=None):
		req, sts = _k._sy(self.request(a, c))
		if sts == 200: return (req if b else _k._s('\n|\t', '', req.decode('utf8', errors='replace'))), sts
		elif sts == 400: self.ex.err('Link gambar sudah usang/ rusak!', False)
		elif sts == 404: self.ex.err('Website tidak ditemukan!', False)
		elif sts == 503: 
			self.bd = True
			print('\x1b[2K')
			self.ex.err('Server website sedang penuh, silakan cek kembali nanti!')
		else: self.ex.err(sts, False)
	
	def ref(self, a):
		h = _k._h().generate()
		h['Referer'] = a
		return h
	
	def findText(self, a, b):
		return _k._c(r'%s' % self.dict[a]).findall(b)

	def json(self, a, b):
		def loader():
			rb = [
'\40\u300a\u2022\40\40\40\40\40\u300b',
'\40\u300a\40\u2022\40\40\40\40\u300b',
'\40\u300a\40\40\u2022\40\40\40\u300b',
'\40\u300a\40\40\40\u2022\40\40\u300b',
'\40\u300a\40\40\40\40\u2022\40\u300b',
'\40\u300a\40\40\40\40\40\u2022\u300b',
'\40\u300a\40\40\40\40\u2022\40\u300b',
'\40\u300a\40\40\40\u2022\40\40\u300b',
'\40\u300a\40\40\u2022\40\40\40\u300b',
'\40\u300a\40\u2022\40\40\40\40\u300b',
'\40\u300a\u2022\40\40\40\40\40\u300b']
			ir = 0
			while True:
				print('\x1b[2K' if self.bd else '\33[32m%sTunggu sebentar, sedang memuat website!!\33[0m' % rb[ir%len(rb)], end='\r')
				if self.bd: break
				_k._sl(.3)
				ir += 1
		self.bd=False
		td=_k._T(target=loader)
		td.start()
		I = self.contentWeb(a if self.alias != 'mt' else (f'{a}/episodes' if a.find('/episodes') < 0 else a))[0]
		ps = ['mc', 'mp', 'mw', 'kb', 'pm']
		if self.alias in ps:
			jd = _k._j(_k._c(r'var manga = (.*?);').findall(I)[0])
			ht = {'action':'manga_get_chapters','manga':jd['manga_id']}
			I = self.contentWeb(jd['ajax_url'], c=[ht, jd['home_url']])[0]
		self.bd=True
		td.join()
		_k._sl(.005)
		self.eB = eval(self.dict[5])
		if not b: b = True if self.eB != True else b
		if b: d = self.findText(1, I)
		else: d = self.findText(0, I)
		say, ara, araa = [], [], []
		apa_ini = r'\-| |\;|\:|\/|\!|\~|\&|\_|\[|\]|\{|\}|\(|\)|\^|\%|\$|\#|\@|\<|\>|\?|\\'
		def you(au, ah):
			def y(o,u): return o.zfill(len(str(len(d)))+u)
			global von
			asc = range(len(d)-1,-1,-1) if self.alias not in ['mi', 'mt'] else range(len(d))
			for i in asc:
				ax = d[i][ah]
				if ax == '': ax = str(int(float(d[i-1][ah])-1)) if i != 0 else '0'
				elif ax[0] == str(0) and len(ax) > 1: ax = ax[1:]
				ox = y(ax, 0)
				if ox.find('.') != -1: ox = y(ax, 2)
				if ox[0].isdigit() != False: say.append(_k._sp(apa_ini , ox)[0])
				else: say.append(ox)
				ara.append(eval(au))
			for n in say:
				ww=n.find('.')
				qq=(len(n) if ww < 0 else len(str(int(float(n)))))<=len(str(len(d)))
				if qq and ww<0: araa.append(y(n, 0))
				elif qq and ww>=0: araa.append(y(n, 2))
				else: araa.append(n)
			hehe = self.fixArray(araa)
			for e in range(len(ara)): von +=  ('"%s":"%s",'%(hehe[e],ara[e])) if self.alias not in ['kg', 'kk', 'mt'] else ('"%s":"https://%s%s",'%(hehe[e], self.web, ara[e]))
		if b: you('d[i][0]', 1)
		else: you('self.dict[4] + d[i][1]', 0)
		global von
		jr = _k._j('{'+von[:-1]+'}')
		von = ''
		return jr
				
	def saveFile(self, a, b, c, d, e):
		def dirSv(p) : 
			if _k._o.isdir(p) != True: _k._m(p)
		dirSv(self.dir)
		dirSv(c)
		end = '%s/%s - Chapter %s'%(c, d, b)
		yi = self.alias
		
		def save(url):	
			total = 12  #variabel total = max thread
			rl = []					
			x = 0
			length = len(url)
			cz = int(_k._C(int(length) / int(total)))
			for _ in range(total):
				if(x + cz) < length: ry = {y:url[y] for y in range(x, x + cz)}
				else: ry = {y:url[y] for y in range(x, length)}
				x += cz
				rl.append(ry)
		
			def dl(ur):	
				for r, u in ur.items():
					try:
						ctx, sts = self.contentWeb(u, True)
						if sts == 200:
							with open(f'{end}/{r}.jpg', 'wb') as w:
								w.write(ctx)
								w.close()
						if e: pd.update(1)
					except: 
						if e: pd.update(1)
						pass
			if e:
				print('\n※ Chapter: %s ⤵'%b)
				pd = _k._t(total=length)
			tda = []
			for t in range(total):
				tdr = _k._T(target=dl, args=([rl[t]]))
				tda.append(tdr)
			for ts in tda: ts.start()
			for tj in tda: tj.join()			
			if e: pd.close()
		
		def mz(pq):
			_k._z(pq, 'zip', pq)
			_k._r(pq, ignore_errors=True)
			
		def Img():
			I = self.contentWeb(a)[0]
			ti = ['mb', 'mt', 'kn', ['mc', 'mg', 'mp', 'mw', 'kg', 'kl', 'pm'], ['bk', 'dd', 'kb', 'kc', 'ki', 'kk', 'ks', 'kz', 'md', 'mi', 'mo']]
			dirSv(end)
			def pmd(pw):
				hmd = self.ref(self.web)
				p = _k._rp('https://www.maid.my.id/wp-login.php?action=postpass', headers=hmd, data={'post_password':pw, 'Submit':'Masukkan'}).request._cookies.items()[1]
				II = _k._rg(a, cookies={p[0]:p[1]}, headers=hmd)
				return self.findText(2, II.text.split('reader-area')[1].split('kln')[0])
			if yi in ti[4]:
				l = self.findText(2, (I if yi in ['bk', 'kk', 'kb'] else I.split('"readerarea"' if yi not in ['dd', 'md'] else 'reader-area')[1].split('div' if yi not in ['ki', 'ks', 'kz', 'md'] else ('kln' if yi not in ['ks', 'kz'] else 'nextprev'))[0]))
				if  len(l) == 0 and yi == 'md': 
					self.ex.err('Butuh password untuk download!', False)
					while len(l) == 0:
						pw= input('Masukan password: ')
						l = pmd(pw)
						if len(l) != 0: break
						else: self.ex.err('Password salah!', False)
				if yi == 'kc': l = list(filter(None, l))
				save(l)
			elif yi == ti[0]:
				y = _k._j(_k._c(r"fff = '(.*?)'").findall(I)[0])		
				v = _k._a.new(_k._ah(_k._hx(_k._pb('sha512', '_0xcfdi'.encode('utf8'), _k._uh(y['salt']), 999, 32)).decode('utf8')), _k._a.MODE_CBC, _k._ah(y['iv']), segment_size=64).decrypt(_k._ab(y['ciphertext'])).decode('utf8')
				l = self.findText(2, v)
				save(l)
			elif yi == ti[1]:
				l = _k._j(self.findText(2, I)[0])
				r = {'encrypted': 'watermark', 'webp': 'jpg'} 
				ll = list(filter(None, [_k._c("|".join(r.keys())).sub(lambda u: r[u.group(0)], (x['url'] if x['url'].find('encrypted') != -1 else '')) for x in l]))
				save(ll)
			elif yi == ti[2]:
				l = self.findText(2, I)
				ll = [(x if x.find('http')!=-1 else 'https:'+x) for x in l]
				save(ll)
			elif yi in ti[3]:
				l = self.findText(2, I.split('"reading-content"' if yi != 'kg' else '<div id="all" style="text-align: center; ">')[1].split('script' if yi != 'kg' else 'div')[0])
				if len(l) == 0 and yi == 'kl': l =_k._j('[%s]' % _k._c(r'var chapter_preloaded_images = \[(.*?)\]').findall(I)[0])
				save(l)
			else:
				l = _k._j(I.split('"sources":')[1].split(',"lazy')[0])[0]['images']
				save(l)
				
		if e: Img()							
		else:
			try:
				if self.eB: 
					a += '&continue=1'
					rc = self.contentWeb(a, True)[0]
					if len(rc) > 444:		
						o = open((f'{end}.zip'), 'wb')
						o.write(rc)
						o.close()
					else: self.ex.err(rc.decode('utf8'), False)
				else:
					Img()
					mz(end)
			except:
				self.ex.err('Gagal memuat website!', False)
				
	def fixArray(self, a):
		arr, ars = {}, {}
		c = -1
		def sorting(x, y): return {p:u for p, u in sorted(x.items(), key=lambda z: z[y])} 

		for i in range(len(a)):
			ai = a[i]
			if a.count(ai) > 1 and ai[0].isdigit():
				ars[i] = [ai]
			else:
				pass
				
		for j in range(len(ars)):
			val = ars.get(list(ars)[j])[0]
			dec = a.count(val)
			for k in range(dec):
				pf = k/dec
				kf = float(val)+pf
				if kf not in arr:
					arr[kf] = round(pf, 2)
		sa = sorting(ars, 1)
		sl = list(sorting(arr, 0).values())
		
		for l in sa:
			c +=1
			slc = str(sl[c])[1:]
			a[l] = sa[l][0] + (slc if slc.replace('.','') != '0' else '')
		return a
		
	def update(self):
		
		def j(e): return _k._j(e)
		def reWrite(a, b, c=True):
			a.seek(0)
			a.truncate(0)
			if c:
				a.write(_k._ds(b))
			else:
				a.write(b)
				a.close()
		def getNew(a, b, c):
			if a != b:
				reWrite(c, b, False)
				return True
			else:
				return False
		def nextUp(a, b):			
			x = open(a, 'r+') 
			y = x.read() 
			z = self.contentWeb(b)[0]
			return getNew(y, z, x)
			
		url = 'https://raw.githubusercontent.com/komiker-py/json/main/update.json'
		p = '%s/update.json' % self.path
		oData = open(p, 'r+')
		jData = j(oData.read())
		last = _k._d.fromtimestamp(jData['date'])
		now = _k._d.now()
		defisit = now - last
		if defisit.days > 1:
			jData["date"] = _k._d.now().timestamp()
			reWrite(oData, jData)
			uData = j(self.contentWeb(url)[0])			
			if jData['data'] != uData['data']:
				jData['data'] = uData['data']
				reWrite(oData, jData)
				status = True
			else: status = False
			oData.close()
			if status:
				result = nextUp('%s/data.json' % self.path, uData['data'])
				if result:
					nextUp('%s/data/%s.json' % (self.path, self.alias), self.dict[6])
			if jData['version'] != uData['version']:
				return uData['version']