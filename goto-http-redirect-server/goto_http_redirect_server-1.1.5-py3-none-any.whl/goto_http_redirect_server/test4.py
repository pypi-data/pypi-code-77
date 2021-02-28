from collections import namedtuple
from typing import NamedTuple
from datetime import datetime
from urllib import parse

# creating default values for Python <3.7 is a bit tedious
# see https://stackoverflow.com/a/18348004/471376
C_base = namedtuple('C', 'a b')
C_base.__new__.__defaults__ = (1, 'B')

class C(C_base):
    def __new__(cls, *args, **kwargs):
        print('args %s' % (args,))
        print('kwargs %s' % (kwargs,))
        return super(C, cls).__new__(cls, *args, **kwargs)


for c in (C(0xA, 'BBB'), C(0xA, b='BBBB'), C(0xA1),):
    print(c, end='\n\n')



USER_DEFAULT = 'user_default'
DATETIME_START = datetime.now()

__Re_EntryBase = NamedTuple('__Re_EntryBase',
                            [
                                ('from_', str),
                                ('to', str),
                                ('user', str),
                                ('date', datetime),
                                ('from_pr', str),  # ParseResult for from_
                                ('to_pr', str),    # ParseResult for to
                                ('etype', int),
                            ]
                            )

# XXX: setting default values for NamedTuple in Python <3.7 is a bit tedious.
#      Copied from https://stackoverflow.com/a/18348004/471376

__Re_EntryBase.__new__.__defaults__ = ('def',  # from_
                                       None,  # to
                                       USER_DEFAULT,  # user
                                       DATETIME_START,  # date
                                       #lambda: parse.urlparse(self.from_),  # from_pr
                                       'def FROM_PR',  # 'from_pr'
                                       None,  # to_pr
                                       0  # etype
                                       )
__Re_EntryBase.__new__.__kwdefaults__ = {'from_': 'kwdef',
                                         'from_pr': 'kwdef FROM_PR'}


class Re_Entry(__Re_EntryBase):
    """
    Redirect Entry
    represents a --from-to CLI argument or one line from a redirects file
    """
    def __new__(cls, *args, **kwargs):
        # XXX: a tedious way to initialize default arguments.
        #      Unfortunately, there is no NamedList built-in. So attributes can
        #      not be modified after `super().__new__`.
        #      Also, overriding via `@property def from_pr(self):`  does not
        #      allow indexing.
        if 0 < len(args) < 5 and 'from_pr' not in kwargs:
            kwargs['from_pr'] = parse.urlparse(args[0])
        if 1 < len(args) < 6 and 'to_pr' not in kwargs:
            kwargs['to_pr'] = parse.urlparse(args[1])
        instance = super().__new__(cls, *args, **kwargs)
        #if instance.from_pr is None:
        #    instance.from_pr = parse.urlparse(instance.from_)
        return instance

    #@property
    #def from_pr(self):
    #    return parse.urlparse(self.from_)


for re1 in (Re_Entry('/from1', '/to2', 'user3', datetime.now()),
            Re_Entry('/from1', '/to2', 'user4'),
            Re_Entry('/from1', '/to2', 'user4', datetime.now(), ('1', '2')),
            Re_Entry(),
            Re_Entry(from_pr=None),
            Re_Entry(from_pr=lambda:parse.urlparse(self.from_)),):
    print(re1)
    print(re1[4])
    print(re1.from_pr, end='\n\n')


C = NamedTuple('C', [('a', str), ('b', str)])
C.__new__.__defaults__ = (# type: ignore
                          None,  # a
                          None,  # b
                          )

