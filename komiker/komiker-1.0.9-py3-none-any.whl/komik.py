import komiker as _k

class download:
	
	def __init__(self, url=None, **kwargs):
		
		self.ex = _k._ex()	
		self.regex = self.ex.read()
		alias = list(self.regex)
		site = kwargs.get('site')
		rar = kwargs.get('rar')
		self.url = url
		if site != None and url != None:
			self.ex.err("Masukan input parameter satu saja!!\n\nContoh:\n\n komik.download(site='mk').generate() \n\n\tatau\n\n komik.download(url='https://bacakomik.co/manga/solo-leveling/').generate()")
		elif site != None and site in alias:
			self.mode = True
			self.alias = site	
			self.lib = _k._l(self.alias)
		elif url != None:
			self.mode = False
			try:
				for i in range(len(self.regex)):
					if self.url.find(list(self.regex.values())[i][3]) != -1:
						self.alias = list(self.regex)[i]
				self.lib = _k._l(self.alias)
			except AttributeError: 
				self.ex.err("Link yang dimasukan tidak ada di pilihan daftar komik!")
		else:
			self.ex.err(f"Tidak ada argument pada komik.download()\n\nurl= ['url manga']\nsite= {sorted(alias)}")
		try:
			self.rar = eval(str(rar).title()) if rar != None else False
		except: 
			sps = '\40' *5
			self.ex.err(f'mode .rar tidak jelas!\nArgument harus dalam bentuk tipe boolean.\ncontoh: rar=True{sps}-ATAU-{sps}rar=False')
		
	def getData(self):
		def result(url):
			getMod = self.getMode()
			dict_url = self.lib.json(url, getMod[0])
			none = '\40\u2022\40'.join([k for k in dict_url.keys()])
			return dict_url, 'NB: urutan chapter => \u300a%s\40\u300b\n'%none, getMod
		
		if self.mode:
			title, url = self.lib.initData()
			return title, result(url)
		else:
			if self.alias != 'mt':
				title = _k._uq(_k._c(r'(\/manga\/|\/komik\/|\/mg\/)(.*)' if self.alias != 'mb' else r'(\/baca-komik-)(.*)-bahasa-indonesia').findall(self.url)[0][1].translate(str.maketrans({'-':' ', '_':' ','/':''}))).title()
			else:
				title = _k._uq(_k._c(r'<h1 class="comics-title">(.*?)</h1>').findall(self.lib.contentWeb(self.url)[0])[0])
			return title, result(self.url)

	def getMode(self):
		ver = self.lib.ver
		if ver != None: print(f'\33[32m\nUpdate: versi {ver} telah tersedia! Silakan download ulang!\33[0m')
		pM = '\nPilih mode download:\n1. Semua chapter\n2. Satu chapter\n3. Pilih chapter a-b\n'
		def cMod(lim):
			in_mode = input('🥀 Masukan angka: ')
			if in_mode.isnumeric():
				n_mode = int(in_mode)
			else:
				self.ex.err('Masukan angka saja!')
			lim += 1
			b_mode = n_mode > 0 and n_mode < lim
			if b_mode: return n_mode
			else: self.ex.err('Masukan angka %s saja!' % ', '.join([str(x) for x in range(1, lim)]))
		def gRar():
			print(pM)
			return False, 4, cMod(3)
		if self.rar: return gRar()
		else:
			print(pM+'4. Unduh dalam bentuk berkas .rar\n')
			mode = cMod(4)
			if mode == 4: return gRar()
			return True, mode, False
	
	def generate(self):		
		login = self.getData()
		x_x = login[1][2][1]
		T_T = login[1][2][2]
		t = login[0]
		h = login[1][2][0]
		e = login[1][0]	
		sad = 'Informasi'
		life = list(e)
		a = f'{self.lib.dir}/{t}'
		fuck = f'Judul: {t}\n{login[1][1]}'
						
		def go(d): self.execute(d, e, a, t, h)
		def the(hum, ani='', ty=''):
			if  T_T==2:print(f'\n※ Chapter: {ani} ⤵')
			elif T_T==3:print(f'\n※ Chapter: {ani} sampai {ty} ⤵')
			return _k._t(hum)
		def oh():
			__ = self.ex
			__.print()
			__.print(sad)
			__.print()
			__.print(fuck, False)
			__.print(False)
			__.print()
		if x_x == 1:
			heaven = e
			for hell in heaven: go(hell)
		elif x_x == 2:
			oh()
			hell = self.di(e, '※ Chapter ke: ')[1]
			go(hell)
		elif x_x == 3:
			oh()
			lo = self.di(e, '※ Chapter awal: ')[0]
			ve = self.di(e, '※ Chapter akhir: ')[0]
			ice= [life[null] for null in (range(ve, lo+1) if lo > ve else range(lo, ve+1))]
			for hell in ice: go(hell)
		elif x_x == 4:
			if T_T == 1:
				dream = e
				for hell in the(dream): go(hell)
			elif T_T == 2:
				oh()
				hell = self.di(e, '※ Chapter ke: ')[1]
				for _ in the(range(1), hell): go(hell)
			elif T_T == 3:
				oh()
				lo = self.di(e, '※ Chapter awal: ')
				ve = self.di(e, '※ Chapter akhir: ')
				def me(ok):
					look = lo[ok]
					veok = ve[ok]
					return [veok, (look+1 if ok == 0 else look)] if look > veok else [look, (veok+1 if ok == 0 else veok)]
				to = me(0)
				tHe = me(1)
				sky = [life[null] for null in range(to[0], to[1])]
				for hell in the(sky, tHe[0], tHe[1]): go(hell)
			else:
				self.ex.err('\nMasukan angka 1, 2, 3 saja!')
		else:
			self.ex.err('\nMasukan angka 1, 2, 3, 4 saja!')
		
	def di(self, list_url, text):
		def gText(t): return input(t).zfill(len(str(len(list_url))))
		I = gText(text)
		if I.find('.') != -1: I = I.zfill(len(str(len(list_url)))+2)
		while list_url.get(I) == None:
			self.ex.err('Angka yang dimasukan tidak ada di urutan chapter!\n%sPerhatikan dengan benar ;)' % ('\040' * 7), False)
			try:
				I = gText(text)
				if list_url.get(I) != None:
					break
			except Exception as e:
				self.ex.err(e)
		l = list(list_url).index(I)
		return l, I
	
	def execute(self, a, b, c, d, e):
		l = str(a).zfill(len(str(len(b))))
		self.lib.saveFile(b[l], l, c, d, e)