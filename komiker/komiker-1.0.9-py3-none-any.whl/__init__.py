try:
	from Crypto.Cipher import AES as _a
	from komiker.ex import extra as _ex
	from komiker.generate import lib as _l
	from os import mkdir as _m, path as _o
	from re import compile as _c, sub as _s, split as _sp
	from json import loads as _j, dumps as _ds
	from time import sleep as _sl
	from html import unescape as _u
	from math import ceil as _C
	from shutil import make_archive as _z, rmtree as _r
	from aiohttp import ClientSession as _cs
	from base64 import b64decode as _b
	from asyncio import run as _sy
	from textwrap import wrap as _tw
	from datetime import datetime as _d
	from threading import Thread as _T
	from binascii import unhexlify as _uh, hexlify as _hx, a2b_hex as _ah, a2b_base64 as _ab
	from requests import get as _rg, post as _rp
	from requests.utils import unquote as _uq
	from backports.pbkdf2 import pbkdf2_hmac as _pb
	from fcntl import ioctl as _fi
	from struct import unpack as _up, pack as _pc
	from termios import TIOCGWINSZ as _tz
	from tqdm import tqdm as _t
	from fake_headers import Headers as _h
except ModuleNotFoundError:
	import os 
	print('Initializing data... ')
	path = os.path.abspath(f'{os.getcwd()}/..')
	os.system(f'python -m pip install -r "{path}/lib"')
	print()
	print('\33[32mNOTICE: All module is done!! Please reload!!\33[0m')
	exit()