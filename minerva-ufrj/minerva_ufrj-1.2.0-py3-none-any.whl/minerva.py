"""Renews books from UFRJ's library through the `minerva.ufrj.br <https://minerva.ufrj.br>`_ portal.
"""
## Standard Library

## Translation
from gettext import gettext as _

## Credentials
import keyring

## Requests
import urllib.request as url
from urllib.parse import urlencode, quote_plus

## CLI
import argparse as ap

## System
import os
import sys
import site
import random

def get_path() -> str:
    sys_path = os.path.abspath(os.path.join(sys.prefix, 'minerva_data', '.minerva-info'))
    usr_path = os.path.abspath(os.path.join(site.USER_BASE, 'minerva_data', '.minerva-info'))
    if not os.path.exists(sys_path):
        if not os.path.exists(usr_path):
            raise FileNotFoundError("File .minerva-info not installed.")
        else:
            return usr_path
    else:
        return sys_path

class Minerva:
    """
    """

    URL = "http://minerva.ufrj.br"

    KEYS = [
            ('LOGIN-PAGE', '"'),
            ('action="', '"'),
            ('func=bor-info','"'),
            ('func=bor-loan',"'"),
            ('func=bor-renew-all&adm_library',"'"),
            ('func=file&file_name=logout',"'"),
            ('func=logout','"')
        ]

    KEYRING = 'minerva-ufrj'

    fname = get_path()

    def __init__(self, user: str, pswd: str):
        self.__user = user
        self.__pswd = pswd
        self.__form = None
        self.__skey = None

    @property
    def user(self):
        return self.__user
    
    @property
    def pswd(self):
        return self.__pswd

    @property
    def skey(self):
        if self.__skey is None:
            self.__skey = int(random.random() * 1_000_000_000)
        return self.__skey

    @property
    def form(self):
        if self.__form is None:
            self.__form = urlencode({
                            'func'            :'login-session',
                            'bor_id'          : self.user,
                            'bor_verification': self.pswd,
                            'bor_library'     :'UFR50',
                            'x'               :'0',
                            'y'               :'0'
                            }, quote_via=quote_plus)
        return self.__form


    def follow_link(self, link: str, key: str, sep: str):
        answer = url.urlopen(link)
        source = str(answer.read())
        data = source.split(r'\n')

        new_link = str()
        for line in data:
            if key in line:
                new_link = line.split(sep)[1]
                break
            else:
                continue

        if not new_link:
            raise ValueError(_("Invalid link."))
        else:
            return new_link

    def _renew(self):
        links = [f"{self.URL}/F?RN={self.skey}"]
        
        for key, sep in self.KEYS[:2]:
            links.append(self.follow_link(links[-1], key, sep))

        links.append(f"{links[-1]}?{self.form}")

        for key, sep in self.KEYS[2:]:
            links.append(self.follow_link(links[-1], key, sep))

    def renew(self):
        try:
            self._renew()
            print(_(f"[{self.user}] successfully renewed."))
            return True
        except ValueError:
            print(_(f"[{self.user}] renewal failed."))
            return False

    @classmethod
    def _get_cache(cls) -> list:
        registry = []
        with open(cls.fname, 'r') as file:
            for line in file:
                user = line.rstrip('\n')
                registry.append(user)
        return registry

    @classmethod
    def get_cache(cls) -> list:
        credentials = []

        for user in cls._get_cache():    
            pswd = keyring.get_password(cls.KEYRING, user)
            credentials.append((user, pswd))
        
        return credentials

    def add_cache(self):
        ## Register in file
        with open(self.fname, 'a') as file:
            file.write(f"{self.user}\n")

        ## Register in keyring
        keyring.set_password(self.KEYRING, self.user, self.pswd)
    
    @classmethod
    def renew_all(cls):
        credentials: list = cls.get_cache()

        if not credentials:
            print(_("There are no stored credentials."))
            return
        else:
            for user, pswd in credentials:
                m = Minerva(user, pswd)
                m.renew()

    @classmethod
    def renew_and_cache(cls, user: str, pswd: str, cache=False):
        m = cls(user, pswd)
        if m.renew() and cache:
            m.add_cache()

    @classmethod
    def list_all(cls):
        print(_("Stored credentials for:"))

        for i, user in enumerate(cls._get_cache(), 1):
            print(f"\t{i}. [{user}]")

class RenewAll(ap.Action):
    def __init__(self, option_strings, dest=ap.SUPPRESS, default=ap.SUPPRESS, help=None):
        super(RenewAll, self).__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        Minerva.renew_all()
        parser.exit()

class ListAll(ap.Action):
    def __init__(self, option_strings, dest=ap.SUPPRESS, default=ap.SUPPRESS, help=None):
        super(ListAll, self).__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        Minerva.list_all()
        parser.exit()

def main():
    parser = ap.ArgumentParser(description=__doc__)

    ## username
    user_help = _("Username")
    parser.add_argument('user', type=str, help=user_help)
    ## password
    pswd_help = _("Password")
    parser.add_argument('pswd', type=str, help=pswd_help)

    ##cache
    cache_help = _("Stores credentials after renewal.")
    parser.add_argument('-c', '--cache', action='store_true', help=cache_help)

    all_group = parser.add_mutually_exclusive_group()

    renew_all_help = _("Renews book loans from stored credentials.")
    all_group.add_argument('-r', '--renew-all', action=RenewAll, help=renew_all_help)

    list_all_help = _("Lists stored credentials.")
    all_group.add_argument('-l', '--list', action=ListAll, help=list_all_help)
    
    args = parser.parse_args()

    Minerva.renew_and_cache(args.user, args.pswd, cache=args.cache)