# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from copy import deepcopy

from iconservice.icon_constant import ConfigKey


FN_SERVER_CONF = './tbears_server_config.json'
FN_CLI_CONF = './tbears_cli_config.json'

TBEARS_CLI_TAG = 'tbears_cli'

FN_KEYSTORE_TEST1 = 'keystore_test1'
TEST1_PRIVATE_KEY = '592eb276d534e2c41a2d9356c0ab262dc233d87e4dd71ce705ec130a8d27ff0c'

keystore_test1 = {
    "address": "hxe7af5fcfd8dfc67530a01a0e403882687528dfcb",
    "crypto": {
        "cipher": "aes-128-ctr",
        "cipherparams": {
            "iv": "dc0762c56ca56cd06038df5051c9e23e"
        },
        "ciphertext": "7cc40efac0b14eaf56f951c9c9620f9f34bac548175e85052aa9f753423dc984",
        "kdf": "scrypt",
        "kdfparams": {
            "dklen": 32,
            "n": 16384,
            "r": 1,
            "p": 8,
            "salt": "380c00457be5fd1c244f5745c322b21f"
        },
        "mac": "157dda6fb7092df62ff93411bed54e5a64dbf06c1aae3b375d356061a9c3dfd1"
    },
    "id": "e2ca66c6-b8de-4413-82cb-52c2a2200b8d",
    "version": 3,
    "coinType": "icx"
}


class TConfigKey(ConfigKey):
    CHANNEL = 'channel'
    AMQP_KEY = 'amqpKey'
    AMQP_TARGET = 'amqpTarget'
    BLOCK_CONFIRM_INTERVAL = 'blockConfirmInterval'
    BLOCK_CONFIRM_EMPTY = 'blockConfirmEmpty'
    BLOCK_GENERATOR_ROTATION = 'blockGeneratorRotation'
    BLOCK_GENERATE_COUNT_PER_LEADER = 'blockGenerateCountPerLeader'
    BLOCK_MANUAL_CONFIRM = 'blockManualConfirm'
    NETWORK_DELAY_MS = 'networkDelayMs'


tbears_server_config = {
    "hostAddress": "127.0.0.1",
    "port": 9000,
    "scoreRootPath": "./.score",
    "stateDbRootPath": "./.statedb",
    "log": {
        "logger": "tbears",
        "level": "info",
        "filePath": "./tbears.log",
        "colorLog": True,
        "outputType": "file",
        "rotate": {
            "type": "bytes",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 10
        }
    },
    "service": {
        "fee": False,
        "audit": False,
        "deployerWhiteList": False
    },
    "builtinScoreOwner": keystore_test1['address'],
    "genesis": {
        "nid": "0x3",
        "accounts": [
            {
                "name": "genesis",
                "address": "hx0000000000000000000000000000000000000000",
                "balance": "0x2961fff8ca4a62327800000"
            },
            {
                "name": "fee_treasury",
                "address": "hx1000000000000000000000000000000000000000",
                "balance": "0x0"
            },
            {
                "name": "test1",
                "address": keystore_test1['address'],
                "balance": "0x2961fff8ca4a62327800000"
            }
        ]
    },
    TConfigKey.CHANNEL: "loopchain_default",
    TConfigKey.AMQP_KEY: "7100",
    TConfigKey.AMQP_TARGET: "127.0.0.1",
    TConfigKey.BLOCK_CONFIRM_INTERVAL: 2,
    TConfigKey.BLOCK_CONFIRM_EMPTY: True,
    TConfigKey.BLOCK_GENERATOR_ROTATION: True,
    TConfigKey.BLOCK_GENERATE_COUNT_PER_LEADER: 10,
    TConfigKey.BLOCK_MANUAL_CONFIRM: False,
    TConfigKey.NETWORK_DELAY_MS: 500,
    TConfigKey.PREP_MAIN_PREPS: 4,
    TConfigKey.IISS_CALCULATE_PERIOD: 30,
    TConfigKey.TERM_PERIOD: 30
}


def make_server_config(config: dict) -> dict:
    server_config = deepcopy(config)
    del server_config[TConfigKey.CHANNEL]
    del server_config[TConfigKey.AMQP_KEY]
    del server_config[TConfigKey.AMQP_TARGET]

    return server_config


tbears_cli_config = {
    "uri": "http://127.0.0.1:9000/api/v3",
    "nid": "0x3",
    "keyStore": None,
    "from": keystore_test1['address'],
    "to": "cx0000000000000000000000000000000000000000",
    "deploy": {
        "mode": "install",
        "scoreParams": {}
    },
    "txresult": {},
    "transfer": {}
}


TEST_ACCOUNTS = [
    b'\x17}\x1c\xdc\x87\xab\xd8\xd5\x15\xc5c\xdfb)M\x0b\xac\xa6\x17B\xf6<\xda;\xf2\x02.,\xa2.\x07\x80',
    b'\x96V\xcbL \xbe\xf3>\xc7\xd1\xe8i\xbc+\xe9t\xb0\x98H\xa7_\x001n1\xfdT~\xb2\xe4\xa0\x05',
    b'\xf3\xa7\xfd\xcdb\xfe\xd9\xff-\x9a\xdezVW\xe7\xf2.G\xf5\xce\x99hq\xa7\xca\x0f\xbe\xd2\xe0_k\x1b',
    b'\x92\x00\x1b\x12\x9da\x0c`7\xed\xb5\xef\xb8\xeez_\x1c\xdf&\x16E\xdb\xb4\xb1\x8aL\xd5;\x1dX\x9fn',
    b'\xc3\x8b\xa0\xad\xddI\x04D\xcb\x13#\xc8\xe3\xa8\xfd\xd9l\xa8\x84}Q\x19\xac\x89\x9bT\x19g4\x85&\x8c',
    b'\xec\xee\xf3+|\xf7\x8e&\xa6\xdc\xff">&\xd4\x00?\xa7\x80\x9b\xea\xa2\xc0Z\'\x9d\x08\xd4\x07i\xf0>',
    b'\x04\xff\xb1-\xfd\xaaK\x9c@\x91\x175\xf2\xde\xc8@\xf4\xfe\x1a^\x1bT\x0czT\xda\x0b+xI\xd8\xe1',
    b'\xb4\x0c\xa9\xc61\x8a\xa2\x1a!\x95\x13\xeb\xc1g\xd0Gm$\xce0J\xf6(\xf3\xd3\t\x8f\x1d\xf2\xac#\x92',
    b'\x11\x96sU\xde+\xf0\xf6\xe09\x1d\x86\xd1\xfb\xf5M:\xd0\xc3\x12\xea\x995\x16 \x93\x95\xdd6\x13\xb9o',
    b'p\x19X\xea&i\x91\xbd\x99\xe70=\x7fc\xabg`(2\x98\xbc\xf0YW\t\xf8\xb3\xcaI\x16F\xfd',
    b'y\xec\xca\xf4\x8b^\xf8\xa6Du6k\x0e\x04\xdfB\xcfYi\xf1z\xcc\xf3\xddP\xe88\xc0T*\x1aK',
    b"\x95\xc3\x08\xd9\xc9\xd4w\xd3\x16\xb0;\xc0=\x15Q]gg\xf0\x18\xf9\xf4\x0e'\x16\x0b\x81\x92~\x8d\x93\xd2",
    b'$#\xb2zv4#\xddOq9(\x99\xbd\xde\xb6p,P\xb8\x80\x07\xf9D\xdd\x1c\x06\xfd\xacF0\xb1',
    b'4\x86\xad}\x04\xfc@\x0188\xa49f>\x97\x18\x05Tb\xd9f\xda\xa2\xa4j\x13Tp\xc3i\x0b\x01',
    b'\x1ee[lv!\x16v\xfc\x0e<\xadP\x91\xda\xc9\xd59\x90\xc1\x93C\xfam\xa3p\x0f<\x06\xeb\xfb\xba',
    b'U\x92\xd1g#\x84;\x80\x01\x02c\x90\xbdPx\x8a\xa5Z\x08U\x02\xff\n\xa0\x94\x1c\xb9\x8c\tr\xf0\x96',
    b'\x0f\xf2I\x9f-x\xa7\xe7\x9d\xba\x9c\xdbKn(\xcb\x85\x82\xf9\xca\x18Hu:\xa2\xef\xa1\x0c\xb2\xfd\x1at',
    b'\xdf$\x89\xe1O\xd9\xe0\xeak\xdd\x15\xf0\xe3}B\xe3\x8a\xca#\\\xfex*8x\xbe\x97\x01\xafu:\xc6',
    b"\xd4^x\x98\xaee\xc7\xea-\xb3\x9c23\xa0\x11>\x87\xb8}\xb5\x90\xf3o']\x01\xc7\xbe\xc5i\x8b\xee",
    b'\x8e\x8b\xc9o6\xe5\x01~\xfb_\x862\x8a\xb8\x03\\\x84\xfe\x96R\x08\xe6\x027:\xd3\xdb\xff=!\xea\xda',
    b'\x0f\x07\xcd]>\xf8\xf4\xaeV\xe8 M\xd4\xcdb\xb6\xa4M\xff\x130\xa0\x9di\xdc\xd7\x0e\x8a@\xcb\xf1t',
    b'\x99\x1eD\xa3\xb8p\xcb\x0b\xd7\x80\xfd\xc6\xe7AN\x9e,|\xea\xc0\x9e\xf6)\xa6\xb0n\xe4\xa6\xcb\x07\x83\xbf',
    b'XG\xf8\x080\x8c\x7f\x977\x9c\x7f4lY\xf21\xfc\x82\x9b\xd1\x0f\xf6\x05kx&\xe6\x91d\x9e\xce\xf0',
    b'\xb2\x9e\xf1\x90\xee\xa5!\xaf*\x05;D#tD\x87aR#\x99\xb3\r\x1db\x98\xf8/=\xb01#\xe5',
    b'\r\xe8\x1a_e\x12\xd7cx\xcdd9k,"}\xf3\xe6\xe6\xf6(\xffH\x01\xfd\xea\xc8j\xf5M%\xde',
    b'%\x010\n\x7f;\xb0\x17\xb6\xf58yp\xa0\xa9\xac\x83\xa1\xfe\x83\xf6\x1d\x8b\xa5\xe4\x0e\xb9.\xcf\x9d\xd9:',
    b'\xa6\xa0\xf2\xe5wHpt\x87Ks\x1b\x91\x80\xb1\xa8\x86a\xfca;\xcf\xfd\x84\xd2<\xcaJ\xa7\xbc*\xce',
    b"i\xa7\n\xde\xc5\xd0T#\xde\x02E'^ _\xfe\xf5\\\x8c\x15\xb2\xa9]\xba\x97m\xd4\x0eHF+E",
    b'\xd3\xd0y\x7f\xafiA\x8dD\x87\x07\xff\x9f\xd9\x88S\x89\xac~\xdc\xc9ZE\x01\xd0\x93\x07\xcdEA\xb2\x13',
    b'&\x8do\x00Cw\x94\xc3h\x0ec\x1aUL\x1dEU\xe27\xd6\xa0\x17,\xd9\xe0=+\xa6\xa3\x81l\xf3',
    b'^\x1d\xf6\xf6.\xa7\x91f\x8d\x90\xaf\x96\xd7y\xd9P0\x96\xde\xa4\x96E\xd5\xae\xd2\xfa_\xdb\xa2J\x12\x9f',
    b'\xab51\x1c\xc5\x05\xa9,-\xd4\xe3K0\xa9Ga\xe5&\xb4\xa1\xfdb\xb9\x83\x7f\xfd\xb6\xec\xc0#\xb2m',
    b'\xb5\x19\x0eh\xa8\xcd\xc3\x12=\xa8\x9e\xef\xce\xbe~\x81\x90o\x18\xfd\xd9\x16\xf8a\xe5T\x0f$\xc9\xb9\xdbC',
    b'\xc1\x16\xd7\xb3H\xc7\xc0\x151\xe5\x00\x10\xbf:\xb8s\xc6[[zE\xc7}\xf7Bv\x1e\x82\xd8_\x1fe',
    b'\xa3\xb7"\x19\xfa0\x92\xd1\x80fS\xf8\x87\x07=3>\x04G^O\x9e\xf1u\xc1q\x85\x11\xd9\xf3~\xed',
    b'\x9dHG\x8b\x86\x0c\x94B\xa6\x15\x84\x9a=\xe7\xa6\xb8pK\x10\xe5\xec\xb0\xaf!\xd3\xfb*\xef\xeaq\xef\xa4',
    b'+^\xe4\xed*B\x7f\xe2\xd4\xe6_\xaby\x9d\xb6]z\x97T\xc1\x88\x10Q\xc4[\x9e\xaa\xb6\xaa\t\xf9\xba',
    b'\xb5\x1fA"\xda\xc8\x19\xc6W8\xa1\xd0\xd30c\xa0\x97j\x93x\x06\x19m:[\x18\x1e\xbe\x04\x11\x08/',
    b'\x00\x0c/\x14[\x0b\xd7V*\x84\x8b~\x8c\xd5B\x00\xd8M\xde^p5\xfb!n\xe4 \x03\xdc\xad\x1cR',
    b'\x03e\xa6\x1e\xa0\xc4S\x9fO\xa8\x14\xc7\xc8\x1d\xf8"\x80\x9eh\xc2~\xbds\xa1D;9\xa3\x9b\xc2z\x1c',
    b'7\x08\x95Ig\x1b\xf1\xb3\x1c\x89\xe7\x85#\x8a\xd3wk\x91L\xcc\x19\xf6\xa7A\x14\x82\xce\xff\xb56D=',
    b'\x95\x16\nkX\xc4\xee4\x10\\\x90X\xedm\xd4\xe3\x06K\x9bG\x98\xb3(}\x01#\x9d)\x17y:e',
    b'\x9c\xa5G\xfa\xe4\x8a\xbe]\xd4\x1d\xc5\xb4j\xba\x86\x8f\xe7\x18\xa3\x88k\xb9\x1a\x1ci\xb5{\xb5\xb3\x97\xf2\x87',
    b"$Y\xeei\xec\xbaa\xfa\x04ja\xdam\x03o\xf9\xed\t\x97\xb5\xaa\x97\x1e\x90\xed\x14\xbb\xc3\x13Q\x12'",
    b'!\xf8\x0c\x0b\x90\xf0ns\x06\xeeLe?\xca#\x17\xe3\xa2{=\xaeE\xd8\xe0\xc97\xee5mL\x99\xf3',
    b'\xf674\x0b\xd4dbr\xad],\xd4\x8bV84\x99D"~G\x82\xad\xd9\xdbr\x86\xa4\xfdw*\x06',
    b'*e\xac~@\xd4s\xc2\xaaj\xd9\x96\xd8Yl\xb9Wt9\t\x17\xe5\x1d[tn\xde2\x12\x1d\xd6\x97',
    b'`\xdf\x01\xe7\xc3\x88C\xff\xbb\x94\xfdf\xaa\x9c\x8cwY\x02q\x9c\xe0t"\x8fC\xdf\xde\xcc\x1f\xe5\xd9\xdb',
    b'\xf1\xfd\xec\x86!w\xf2\xc1\x89\xcc\xe8\xc08\xf3\x8c]\xf0\xae\x112\xf5\x81\xea2T;\x97)\xbd\x000\xa9',
    b'\x9f\xbd\x9c\xf2\xdb\xbe\xc1\x87[4\x03\xa4\xb7\x92\xd85\x1f,\xa0\xcb\xa3SyI\xd3\xa5{\xe1\xdfkt\x17',
    b'\xa3\xc3\xdd\x98;\xe5\xb38g\x9b\xa5\x92\xae\xafm\x14P}r"\xca;\\d]\xda\xb0\x880\xdf#\xb0',
    b'\xff\x8c\xd3\x1f\x14\x89\xaa\xb5k\xe6 M&\xa3\xd0\xdf\x1a\x97\x82"\x064\xeao\xdb\xf6\xc4]\x94\xeb\x87\xd9',
    b'\x9f\x93\xbe\xc9E\xcen.xn\x89\xa7HV\xa2\x80Y~X\xf1\xd0\xce\xd3\xb8\xf5\xbf\x05\xd5\xc0IG\xe0',
    b"\xb1{\x06X\xba\xb7\xceQD\xa3\xa7X\x04'\xb8qu\x10\xae\x87\xc2[F\xc4^\xcd>b#s\xd5\x01",
    b'${\xc7#\xa2\xb5(\xbc\x92>H9\r=\xaeS\xfbR*\x00?\xd2\xeb\x86WL/\xda8\x03W\x1d',
    b'c9I\xf9\xfe:\x1b%\x1d\xa3t\xf2\xa6\x9b\xb6c\x00CZ\xe6<\x10\xf5\xf31\xea|\x9c\xe3#\x99\x10',
    b'\x88~\xab\xec\xed\xdf.E\xd3\xae\xb5\xe0\xa8\x19,\xdd\xba\x89\x95\xf0\xc4\x93\xe6\xf2\xec\x1aW\x8c\xe0\xf9`\xec',
    b'\x89:\xbf]/\x9d\x9e\xc25~\xb1;\x912\xec\xec\x91\xd5 \xed\x8b\xc7\xf0\xc8\xdcn2S\xf1\x17-V',
    b'\xc1\xfc\xbd\xaaM\xa9\xc74\x82D\xa6_\x1bl&\x95\xaf\xbc\x93YO\xe3\xf0\x0eW\xf6f\xf4@\xe0v\xe1',
    b'A\xe9\x7f9\x85\\\x80d8C}$w|\xb2\x18\xdc\xff\xb3\xaaY\x8e%e\x1d\x9d%\xd8&A\xb1\xa9',
    b'Dr8\x1b\xab\xed\xe4\xd5\xb5\xdc3b\xb8\xf3\x81\x15\xf0\x0b;\xad$\xce\x86\x1a\x8d)\x1eVBi\x8b\x84',
    b'\x0b\xe4\xf5\x8e\xdf\xb5\x0b\x9a\x8d\xee\t\xd5W\xe96\xa3\x9c0\x98\xaa\xcc\xe3a\x07\xd93\x02\xfd\x89\x94+\xe1',
    b'I?J\xa4g\x89DGS5m\x96.>\xbenw\xf8+\xf7\xec5\xb8\xde \xf1\xeey\xce^\x16\xd8',
    b'\xc8y(\xb0\x9fn\xca\xb6\xc2~\xf4\xe0\xc2|\x0f\x1aTF\xf6l\xaa~7j\x18^\x08\xc5\xd9\xdf$\xb0',
    b'\xc8\r\xcc\x8aQ\xda\xb1\xe8\xef\x1c\xb5v\x01t\x7f\xea\x96/\xd0\x08CJO\x99Z6\xc2\x13P\x1f\xf5\x98',
    b'+rR\xbf\x03\xd7\x87\xe2;/\x992\xe4\xcb\x8c\xbc\x88i\xc8\x81H\x82Z\x8e\xea\xdc$\xac\r\x84\x017',
    b'\x81o\xf6\xc1\xd0\xee\x12\xaf\xc0\xec\x0b\x0e\x01\xa2a9Y\x95\xbc^\xabMg\x87\xd3\rN\xcb`\x88e\xbc',
    b'!\xcdO}\xb6\xd3\xc27\xfdl\x16w0\xd1D\x83&Ph\x04\x06\xf4B\xf8\x1c\xba\x00? \xea\x0e1',
    b'9t\xbc!O;\xa3\x85\xf4<M\xffQ\x9f\x04W\xff\x00\xb8\xd3C\xf5\x88\xef\x83i\xb4#\x16X\xed\x8d',
    b'\xa2\xa2\xb2\x82\x9e2@\xcf\xe1\x05\xb1\xdd\xcb\x96\xd0\x95\xad"\x8d\xf8/O\xeb\xd7\xdf\x14\x12#K-\x94@',
    b'A\x87\xaeb\r\xee\xca.\xb2\xe8\xf8\x0bU\x7f\xa1l\xb5\x0c= -cLY\xbesu\x0f$\xe7\xa7T',
    b'\xfe\xee<\xbd\xd2\x1f\xa8Q\xb1\x9a$\xe6\x95o\xa9u\xa8Y\xec#\xb4\xdbK]\xb5{\xd6&\x1d\x12\xfe\x94',
    b'\xa8\x15P@\xa2p\x84\x91@.\xd1\xcc\xb0\x13\x14\x03\x91\xca\x0c\x9ez"\xa4\xdfG\xa3\x86Q\xd0\x10W\x03',
    b'\xd87W\t\xdc<}+\x87\xdeT\x9a\xa3\x08q\xeb a\x9d\x06\xaf\xd9c\x16\x16\xf8\xb9y\xc4{WG',
    b'^>l_\xf8\xf6}\xcfi\x03\xfb\x17=P\xa6\x86\xf2\x91\xff\xa20Q\t<\x8d\x02\xbd\xe1qusO',
    b'\xf6\x83R\xb9\x02\xa0\x84\xc1-sm\x83\xfcd\xd1\x8a\xe5\xe5{\xc0Gz\xbdj<\xb2\xe7!\xed\xa9\x9f\x16',
    b'\x06f\xdb0\x90\x7f\x97A\x8f=j#^L\xb4\xf9&K\xa1\x99g\xf0\xa1l\xdbm\xc5\xfb\x12\xa2\xb7+',
    b"P\x0e\xc8\x98G\xc3D\x0f\xdd(D\xe3\x07'F<\xa5Y\xf7\xd7\x08\x08O\xdf\xd9\xb6\t\xcc2|*\xa5",
    b'\xaa\x94\x97KO\x19\x7f\xee\xaa\xc5\xc5\x04\x0f\xf3\xf2|\xc5\x075EMY~\xb3L\x08\x17nR[\xc2C',
    b'\xf9\xdf\xbf\xdf;v\x87\xbb\xd4\x00J\xa9\x8dJ\x0f\x11 \x82\x7f\x9c\xbd#\xe8&3\xda\xf9p\x0ehx\xe1',
    b'\xf1\xc3\x9e1]b\xc6_\xc0\x86\xcc\x96+\xa9\xa1\xe5\xea\xc2\xad\xb4\xbb4=mSe\xf8$\xc7XE[',
    b'G\xc0\x9f%h\xe6\xcc/\x8d\xaeptN686!\n\xd5\xd3g\xd4;$\x98B`a\xd8\x99P\xc0',
    b'\x0e\xfb\xf4\xc2\x05\xe8\xdc\xe7qK\x90s\xd6\x8c\xd0\x89\xa3\x04\x89\xdd\xc8\xe6_\xc6\x02<\x95"\x9b\x9171',
    b'\x05\x186\x14\xe4\xa2\x1f\x12\x92_>\xaah\xc4\x97\xdd\x98\x10\xbdB%\xd5\x0f\xd0\x96\xafB\xc6\x1b\xe5/M',
    b'YdR\x1e\xd5\x0e\x02M\xe3\xfb\x00\xc1v0\xfd=\x8ck\x14)H\xad\xdc\xf1\xf2M:\x14p"_\x8d',
    b'r7ax\xca\x9b9\x03\x15pl\x1b\xd0\\\x12\xd5A\x18Fb\xf1\x95\x14\x9e\x96\xe8\x97M \x1d#\xd2',
    b'\n\xb8\xd3b\x06\xbe\r\x1b\xc8s\xdd-r\x8bA,WW]E\x1eE\x96\xbek7N\x1d=}\xd7\x98',
    b'\t\xa3\xa8\xdc"r3]\x14H\x7f\xf4\xeeo\x18\xcao%"\\\x8fH\x9a\xaf\xf8\xc3\xc4x\xce\xa92\xb4',
    b'\x88\xce\xd1[\x8c\xe2R]\xd5\xf9\xc5\x80\x10nn\xf8\xaeN\x18\x0ct\xe83\xab\xbb\x05\xad\x00\xea\xcb)"',
    b'\x18}\xb7\xca\x81M\x86he\xb8\xfb!\x81\xce\x1e8bA\x9e$\xa7["\x8bG=\xf0\x92\x1a\x80\x93\x9d',
    b'}\xdc\xed\x1f\x94\xd5j\xe1\x98\xd9\xafOy@\n\xdb\xc9&>I~\x1d\x86\xa4\x8d\x1a\xe3\x90\x06\x8b\xe1&',
    b':z*\x80*9$\xfc\xe9V\xdb\xb0H\xc9\xc7\xb2\xc2\xc4\xdc\xe2\xba\xc7\xdbm\xc6u\xafm\xa8\xa2\x8f\xd0',
    b'2\xef\xee\xfb\x03\x16\xd3PP\x96t\x8f\x07g\xd0\xf5\xab\xff\x1a~f\xb1\xc5\x1e\xfa)\xd8]\xf0=\x01\xed',
    b'\xde\x18\x9a\x862\xe3\x17\xe7"j\xde\x84%\xdbo\xf0\rg\x9cp!#\x9d`k+\xb1\xd50<\x04\x80',
    b'\x16B*\xc5=$\x8c\xca\xc9l\xf1\xe0\xe0\x10\xe9\x9d\xe9] \x9c\xb6\xb5;\x82\x13c4\x93K\xfc\x8cc',
    b'z\x06+\xec)\xa1\x91\x95J\xb50p\x90\xdeZ\xbb\xe4o4\x92d\xb5\x96/v\xc3\x16\x1f\x88Lr\xbd',
    b'A\xfcx\x9d\xf3\xf1\x1d;\x81X\xe6\xd5.N\xdf\xeb\xd6\xb1\xc3\x9b \xb2\x8b\x9b\x9f\xd7q64\x00\x18}',
    b'\xad\xffY\xbf0\x9e\x92\x7f\r\xb7\xc5\x00\x8c\xf4\x0f\xf9\x0c\xcc\x92\xa2H\x8e\xd4+\x0c\xdc{\xa9yj\xc7\x93',
    b'\xec\x8d\xfbu\xc6\xcd<\x99\x07p\\\xae\xfe\xa2\xf6M\x07\xb7X\x02?Z\x97\xc6Qs~\xd8c\xfc\xd1\xe9',
    b'\x83\x87\xeb.{\xb3F;\xe8\x96\xe2j\xcf\x8fh\xb8\x88\x89\x9f\x06\xdc(V\xa6\x07\xf4(\x89Z;\xdf\xf2',
    b"\x8d\x8c\xc7\x1e6\x9e,@\xa5l\xd9'\xd5fB9\xde\x80\x96\x7f\x91\xe1\xd8\xf1\xfa:N\x1b\xc3\xa2(\xc8",
    b'cdj\xa1\xbe\xfd\xf1Ay\x93\xdb,y\x1c[\x05\xb7x7\x1a\x9d\x9cd\xbeR\xbf\x15\xfc\xdc\xc8\xd6\x88',
    b':\x97Y\x1b\xa9\xd3\xe7Y\x9c2\xce\xd9t\x9cm\xc9\t?9\x0fb\x0b\xb4\x04s+\xa7q\xa8CX\xa7',
    b'\x0c\x85n\xff\xb2\n\xefS-\x95\x13\xfa\x95\x90\xc1S\x0f\xab\xf8\x0b3;\x83\xc1@\xeb"zn+7\xe6',
    b"\x85b\xc46\x92\x95\xaea\xd7d\x1e'\xf1\x11\xd8h^\xf1\\\x8b\xd2\xc4Dq\x0cj:h\x07jU\x98",
    b'\xf73~\xed!9]\xd6W\x01\x19\x05\x87\x80G\xb8\xe1\xc2p0Q\xe6\xabb\x16u\xd2\x0e\xa9\x9c04',
    b'Z\xfdr\xc2\xb1B\xb9X#\xc1\x97\x9a\xd8\xd9C\x8b=\x82\x94ko\xfc\xed\x04 iB\x15\x08\x1cV\xfa',
    b"\xf5`f[\x1b\xc8\xdc;/\x90\x82\x1e\xb3'\xbd\x82KC\x82\xbd{\x18\xf14\x81\xb5\xa86\xe5JgR",
    b'\x99?1\xc6\xd2(Lf?T#G\xbcU\xb6H\x96\x1aH\x96\xbc\xbb\xbd\xd9\xc5{\x0e\x91\xe9Z\xab\xc1',
    b'\x1b5_\x1f\x0bi\xd1\xd9\x1fRUe\x8f\x13\xd5!\x8b_V\xb6(\xac\x1d\xf7\xc1\xdc\xdc_\x02E\x0bO',
    b'c\xb0\x01\xbfR0iu\x16\xb8@\xef\xe7_gi\xf0\x1cq\xfa\xeeo\xdflDy\x00\xba`B\xaf\xb3',
    b'_\xa2.\xaa\xad@\xaa\xa2\xa1\xc9\x0e\x1a\x9eH\xf9\x7fA\xd4B\xc5\x8b\xd9\x17\xfb\xb8\xc0~\x04\x82n\xf4\xad',
    b'\x03\xf3\xb0\xa1bu\xfdD\xbf{u\xd1\xdb\r\xbc\x11N\x86\xef@+\xad\x81HK\xfb\xcd%T!4\xcf',
    b'r\xce\x15,l\xb4\xe7C\xcb\x063\xa5\xb2"\xdc\xbcoi\xc2\xa0\xa1\xb2\xa0\xdeY\x14b\xc6\x1e\xc2\xf6\xaf',
    b'\x07\r\x00Z\xec\xc1l\x0f\xd0\xc8mw\xdb\x03\x079\xa4\x16v\xc5\xdd(\x83\x1b\xe4\xab\x86\x9d9\xf1P\x13',
    b'<\x13=\x91/\xb7\xe4\xb4\xa3\xa2\x027\x8b\x9b6\xfa[X\x0fJcm\xa0,\xf68.\xc9w\xf5J\x14',
    b" \xe6V\xdb\xda'\xfe\x9ey\xc3X\xed\xa2}\x17\xc3\x1a\xa5w\xdc\x92\xd8\x81\xed\x0f@`pD\x9e\xa8\xbf",
    b't\xcc\xc5j\xee\xea\xc9\xe93\xf1V/~\xe3\n<\xee|\xb7\xbf\xda`\x8e\xcbY\xfe$\xaf"\xe5\x06\xcb',
    b'\xf7G\xb0\x91\xb0\x8d\x15\x05\xd6ik?\x04~R\xef\x96DP\x9ap`\xa5\x01\xbb \xd6%\xf2\xb6`\xed',
    b'0\xb37\xb1\x91\xe2\x81\xe0K\x07i\x0f\x03m\x1d\xabL\xe9\x07,\x19\x96\xaf!@\x1bzg\xf4\xbc\xfa\r',
    b'w\xae{\xbey\xb3(6bQ\xf2p\xa5\xbd\x1c9\xba\xd8\xf1\xd5\x83\x80\xa5\x8d\xcfcrA&O*\x1d',
    b'[*\xeb\x80\xde~\xfb\x99\xb8\xb4\x89\x1a%\x9a%h\xba\xd3\xa4\x8a\xa3\x01\x92Q\xf9r\xcbe\xb2u\x15\x83',
    b'\xa1\x9f\xe6C\xe4qQu<\x06\x0fW\xad\x01\xdc3\xdc\x11\xa0O\xe5\xd8\xf3\xcc\xc2\xca\x8a\x94\xc4\xbb\x01\xb0',
    b'\xb3\x9f\xd7\xd9\xf1\x98\xf3\xcb6\xc9n\xc7\xd1\xf3\xea5\xd8\x18\xe5\xca\x04\xa6e\x97\xa5a\x99jc=q\x1f',
    b'\xb2\x91&\x96wLHy\xd7\x04\x8f\x8d\x82\xec\xa3\xc8\xc1s\xf7w\xae\xf7\x9a\xdb`J\xe2zed1\x15',
    b'\x8b\x819\x8d\xb7\x98L\xcb\x05\xd8\xe5)\xe8\xcd\xa6M\xed\xef.\xb2\x8d\xbaW\x16")f{q\xb0h\xfa',
    b'\x85\x97\xf4\xf1\x0e\x9f\xbf\x95\xde\x15\xad\x10\xc7\xb17\x13\x95\xddq\x98\xb2{o}\x97>\x07,\x10\xebF\xf9',
    b'\xf9\xd0\xa0{\xc8\xf0V\xb4\xfc|r\xc3k\xed\x05\xf5\x058\xfe\x01\xcer\x84G\xbe\x9b\xd0\xfd!\x99\xb0\xe0',
    b'\xab:\xde\xd0%{q\x88\x87\x96\xc1\xee\xfe0;xW\xe1k\xa8\x16\xe3WW\xeb~\xce\x826>-\x9f',
    b'n\x1cg\xd7\xbd\x15\x8b\xf6\xe2$<\xba\x98ABq\xba\xe0\xcf\xfc\xf5v\xa3xG\x8a\xf2\xb2(\\~\xce',
    b"\x0e9\x7f-\x82\x912\xb9\x05\x10\xa26\xbdw\xfeP\xbd+/\xd1\xa6,\xdf\x89\x0f3~'\xddi\xac#",
    b'\xc2\xd3\\\x14\x12I\x8e%\x8by\x9c\xff\xf3a\x81\x0b\xdcv\x15\xedY[\xac\xa4\xe4\xa3\xba\x90\x13,\xb4\xcf',
    b"\xda\xf4\xc5\x83EEt\r\xd2\xc3\xcbUw\x9b\xc8\xab\x838\xa7\xa7\xe8'T\x98\x1e\xc0\x9d\xcc\xfb\xa2\xf5z",
    b'\xaf\xed\xb8\x85)\x7f\xe9\x85o\xe81Nk\x95M;\xed\xa3j\xbf\xb5ez\xfb2\x10\xab\xf1\xacEW\xc6',
    b'\xb2\x99\xfc\xb0\xee\xa2z\xe1\x87\x19A\x8e\xd8\x91\x94\\\x89VQP\x83\x10\x1arR\x95\x10\xae\x17w\x94%',
    b'\x8d\x84\x04\x90\xfa\x86\xdfx:\xd3(\xd32F\xee\x151\xbeD( \xd7%\xbe\xf0\x9c\x87`\xf3\xc1}N',
    b"`\xfc\xd6WCMVh\x19\xb2\xc2\x0fz(\xbd'\xc9\x99\x12\x83\xacl\x1c\xfa\xfb\xf9\xdeq\x15nt\xa9",
    b"\x853\n\xee\xe63\xe7HI\x10n\xbft\x13\xbeM'\xe0g\xb7Bf\xfa\xb8\xff\x11#0\x9b\x8e\xd8\xfb",
    b'\xab,<p(\xf6\x9e\xe5c\x1b\xbe+\\\x02\x99\xc6\xe3\xbb\xb5\x8e3\xb6\xc56\x19~\xd7\xbaY\xd9\xfd\t',
    b' Z\xf3B*V\x04\xe8\xbc\x98\xf8\x8e\x0e\xea\xd0\xe6G\x03\xa0HV\xc6Mh\xb4\xd4\xa2\xbd\xc5!|\x82',
    b'jG-\x08)\xa2\xc9\xfb:\x17\xd8\xca\xf0\xd8b\x13\xc3/x\xebA\xd8\xf8]\x02\xafQv\x93\x02\x1e_',
    b'\xaaqL\xf1\xb4\xf8\x03;\xa3\x96\xa4\xff\xe5#\xb8\x04\xe6\xda\xe1\xbe\x00\xf4X\x04W} \xd9\xf4\xa8\xb8\xb5',
    b'2\x84zJ\xbc|\xedGOq\x1cpz\xa5\x82%5G\x9a\x1d\x9e\xb4a\xe0\xd3a\x06\xb1\x85\xe8\xdc"',
    b'\xdbX\xb0\xe0\\\x01\xc14:\x93h\xfb\xf0\xa44\xc7aW\xb6\x07Ob\xbf\xc6\xed\x84j\xb9.\x0f7B',
    b'\xe6\xe9\x1c5W\xf5\x07\x0eROBJ\x16\xe0do3kiIKe\x14\xfb\xc2\x9eI\xd1ZE\x1a\x07',
    b'\x05iZ\xa9\x07\xe2`\x93\xc8\x0b\xf9\xb5d\x87\xdfjE,qyQ\x9c\xd8?\xc2\xe0^\x181P\xc9N',
    b'\x13\x1aG~\x1e\x11\x98UB\xc2\xb0\xbd"\xa2\xad\x921B\x1a\xcb\xd6\xea\xf7\xa9\x99\xda=\x95\xad\x0b\x05\xa4',
    b'0L\x11\xa4\xf0\x86e\x05X\x1c\xceh\xa3s\xa8\x1f\x85Y\x15\xfa\x8d\xd4 +\x94\x8e"\x83\x1b\xdeW\x02',
    b'\x06\x8b3$3\xd2\x11g\xc4\xa1\xaa\xaa\xa1\xdf%\x7f\xd1\\p0a\xa1\x00\xbd\xc1{\xc2\x02%\xd8]\xbc',
    b'\x1b\xc8-\tL\x1d\x8d\xa7g\x9d\xfd\x82\xe0%r\xd1\x89E\xf8^\xaefv\xe0k\xc2\x07\x9b\x05\xfe\xd6>',
    b'\x08\xe3\x81\xc5l\xb1YP$j2\xc3\xe0\x8c\x87v4\xdaD\xcc\xb0\xd1\xaf\xff\xa6%nB|N=\x13',
    b'\xb9\xd7\xbc\x81\x89t,\x97\x86\xe1\x1f\xb9\xe4\x03\xda\xca\xfd\t\x17\x97n\x1d\x95\xe1:">t\x91\xe2\x06\xbf',
    b'UD\x1d\x91\xd4\x99\x1b\xe9<\xba\x9f \xc3v\x11\xa9\xc9L\x00s8\xdd\xf2\x95\xfaC\xbc\xd5\xd4|\x00O',
    b'G\xd3\xa1p\x81L\xcb\xe2I\xe7\xce\x0fI]\xe1Y)\xfa\xfc\xde\x82X\n}\x1aq\xdc[\xe5\x89\xf3\x80',
    b'\x92r1\x98\xeb\x19\xca[\x8cW\x1f\xb13\xee\xf4\xf3m\xaec\xf9\x07P\xfd\xdb!\xa6\xa33\x0f>z\xdc',
    b'\x14w\xbdp\t2\xc3\x16\xf8]3\xe8]\xb8\xc3\xdf|Z\xf3\x05\x11\x8cl\x1er\xb4\xc1P\x17\x82\xeae',
    b'\x1b:\x1c\x03\xcb|\xa8s\xc6\xfe\xce\x92\x11\x84\xcd\xfc\xf7\xe1?\x04E\x04tT\x90\xdb\xf0\xac\n\x94m\x07',
    b'b\x1d\xb9g\x96LS\xady\xbd\xa0\x10\xce\x03Z,\xfe\xee\xf1\xfd\x19oec$!\xc2\xe4p\xb2\x13\xaa',
    b'\x81\x9c\xfa\xdf\xedc\\f!\x82\x95\xa0\xd6\x9fH\\\x14h(P\xc7\xec^\xc1\xd3\xbf@\xc0\xe4=\xdad',
    b'\xb4\xcf\n\xae\x00\\\x97\xff(]\xca\xb0\x84\x0b\x97.\xf6\x1f\xb52h\x01\xe4\xdbE\x9d\xddk\\\xb5\xdb\xa4',
    b'H\xc8J\xb2\xd6v\xbaj\xccy;j\xad\xde\xa4\x1a\xd5/\x93\xb9\x05\xf8(\xf9\xc8\x07n`\xbc:\xc30',
    b'0<c=]v\xd6\xa8(\x14\x90\x9ej\xc7f|\x81\t\xb4\x12+\xa1\x8aW\x0c\x13\r\x17m\x92j\x8d',
    b'\xcf#\xb4\xf9\x88^\xa2\x15dQ\x82ibL\xa1\xe7Sh\xfa\x02\xd3\x9cLc\xa4#"hl\x9fW\x9a',
    b'BO\xe2\x14+tK{\x9c\xb6 \xc6\x95I\xa9\xc1\xdf:\xad \xe9\xd3\x95e\x08\xb1\x86\x9d(\xebp\xae',
    b'\x9eq\xd9<^;\x08\xf4\xfak\xbf\t\xa6\xef\x8cu\x93\x08=\x16\xd7P\x80\x88[z\xa5[Cne\xdc',
    b'\xbeN\x1b\xb2\xbf\x99\xf9H\xbd\xedG9\xa2Y\xb9l\xc1a\xf0\x12\x8b\x80Q\xbb\x97\xad\x93\x15\xf2J\xb5a',
    b'{9Y\xe0\x86\xe7yAX\x0cn\x84\xda\xd3\x08\x89L\xdb\xe4\x87\xd2AV\x19d\xfa3Mt\xee^f',
    b'x\xcaGP\x08\xa8\x1a\xf0 k\xcd\xda\xb6\xeb%J\xb7\xb8;\x9c(\xbdGD8=;\x04:\xa2\x84\xfc',
    b'\x80\x95\x1c* \x93\x1b5l\x9f\xddF\x82\x7f\xcd7Y\xa2\xa2\xc8.\x98w|\xf4\x0cu\xdb\x9e\xa3\x9c\xd5',
    b'\xfd>\xaeVy\xc1\xc8\x0b\xac\xf9*h\xef\xd8`\xa7s\x91\xcb\n\x94\xef\xb1,\xdc%\xbd\xf6\x9f\x93\xd2\xe9',
    b'\xb8\x9a\xf1\x1b\x93\xccb\x89\xcf\xb7\x10\x1b\x94\x07H\x87\xaa\x1b{\xf7\xaf\x81\x04\xbbK\x87\xcdm\xc9\x9e\xb32',
    b'W\x04\xa9\xc4\x9f\x8f\xc5\xf3\x89 \xe2\xe7\xe0\x86\xa8Q\xbe]\x04{\\\xb2\xac\x0f!\xa5^\x96$\xfc{\xce',
    b'X^*\xad\x93\xf8\x05\x1a\x82nFf%q\x9a\xab\xe7:\xfa\xc3\xablp\xc5Y1\xf9\xc1\xc1\xec\x8aF',
    b'H\xd0>P\xc1\x890\x05Hy\xc6\xdf]\x88`\xcbcU\xdd_\x80\xb47/\xb4O\xfdHO8)\xfa',
    b'C\x12\xa9\x9e\x1e\x1e{<T\xe9\xe1\xc4\xbb\xdd\xba\xd6[\xd2\x88X\xe6Hu:\x82a"\x1c\x87\n\xd5C',
    b'\xcc\xbf\xc2\xa5\xa7w\xa2\x16\xd9\x05\xc3\xfdT\xfb\x17\x87\x81o-\xa0:1\x02\x8a\x11\x1d2\xab^3\xd2\xf7',
    b"\xf7\x84co\x88\xd4j\x13S\x9a\xb9'\xff\xec\\f\xb9\xb9]\xdc\xb8\x9765y2\xa6\x13C^M\xde",
    b'Q\xbf)\xe3\xed/\x83z[\x82B\x93jZ\xfd\xf2B\xd3J\xc8\xcb{\x1fgN4\xba\t@Q\xc6\xf0',
    b"!\x973p\x13\xa3\x8b\x9c\xa6\xd8\x1c\xbb\x8c\x8e\xedJ\x05\xca\xa0'\xdd\xfe\x8b\xdaN\xe1\x05A\x8a)\xb0\xc3",
    b'a\xa9\xca\xa7Og\xbe\xb9\x1e\xfb\xc4\x99\xaf\x9fG3k\x7f\xde\xab\xc9\x87\xa5t\xbe\xc0\xcb;=8\xbf\x02',
    b'f\xf3v\xcb\xfaf\xda\xa1\xde:\xce\xf4}\xaa\x8b\xaa\x7f\x85\xa2\xd4\x8b:\x0f\x8d\xb9\xc14\xaa\x8a\x922\xa9',
    b'\xb2,\xe4H\xf7\r\x8d2\x9c%:\x11\xca\x82\xb1\x87\xc0\x8e\x88\x13\xf11 \xe33FDa\xbc\xf3\xceK',
    b'\x7f$\xc9\xfeu9\x1e\xb7b\x8e\x97\xc5\xd2\x18\xfb\x08Y\x00\x98TA\xa06\xc0u\xb5\xd4A\x98\xceX\x86',
    b"\xcc\xca\x08S\xe0\xb3\xeb\xb9N\x0b\x12\x8f\x00\xaeB'\x9b6s\x07\x03\xdaI\xc7\x96\xaf\xf1\xf7\xd9\xf5.\xf2",
    b'\xb6\xaf\x07x\xba\xd4\xfb\xf0\xf4\x81U\xe6\xd3\x94-D1\xcbx\xa5\xf4\x8fK\xaf=\x99\x83\xc0\x14_\xae\xed',
    b'8\x1d\xc5Dm\x8f\xfe\x06YCO\xbc\xfeW.\x13\x12\x83\x8eF\xac\x19_\xfbY\x96\x91\xa7\xd1\xb5\xa0 ',
    b'\xa78\xe9\x0bM\xd8\xb8\xb7\x0f\xd9 \xeb\xc5\x92\x98=\x9djg\x9fmx@P\xa1s\x92\x98\x1c\xd0p\xe4',
    b"\xd1\xfdw\xc5\x83\xe8c#+ F\xced\x92\xea\xc5\xc1\xa5\x7f'$\x06F\xcf\x8c\t\xf7Ts\x84\x19\xa4",
    b'\xdb?6\x07\xfe\x8d$\xc5K\x8c\x12^,F?a\xf2\xd9\xd7B\xd0\x9d\x05(\xdf\xc4\xe0\x1ac\xbf#\x10',
    b'\x7f\xc78\x83\xeb>{\xe6\xceu\x04\x8b\xfd\xa6o\x07\x10{]~\x1e\x9e\x93a\xee\xecP\x8eK\xb0-\x0b',
    b'\xbf!?\x94\x1a\xd9K\xdd\xb3sg_\x19jN\xdc\xc4t\xf56\x0fG\x9e\xba e\x0ba\xd2\xde\xfa\xe4',
    b'\x87\x15\xfc\xcbflz\x980\xf1\xa9\x0b71\xcd\x8eG\xbb/q\xf5\xd9\xf7\xfb\xcc\xa1\xba\x1fh\xa8\x1fp',
    b'#\\n\x7f\x92\xf39\xfd\x1d\xf5E@,[\x0c\x08\xb9^\x80\xea\x19F\xbcv\x1f\xcc6\xb0\x066a\xb0',
    b'\x8c+\x1dd\x82\xbc\xbdb\x1dF\xac\xa1\x9e\xdc\xaa\xf0\r\x8b\xa57}}6&|\xf5>g\xf5/\x0f?',
    b'3x9=\xc6\x1f\x15vB<{\x9d\x19e\xa5\xac\xe1\x8a\rkAPQE\r\x1e\xfc2\x104\x03\x9a',
    b"\xf1\x16\\\x9a'fo]\x893F\x15\x8f\x03\x8b\xb0\x9fj\x93\xe4\x1b\xae\x7f\xc0\xd6dz5-/\xbc\xce",
    b'\xee\xe8Z\xca\x1c\x90\xa6H\xab\xc7\x033\x86/cY\x12\xc0\xe2,@v\xda\xe6\x1f\x99\x0f\xf7\x87\xeb\r5',
    b'\x90\xfb\xf0L\x06&\x9fWi\xa7\x9b\xf3\x7f\xc4\xe9\xc2\x8d\x11\xac\xc4\tu\x18\xd6\xf4\x82\xca\xc6=w\x19p',
    b'\x84\xe5A\x8c"\xf0\xe4\x1co,\'\x02\xca\rw\xacG\xfeF\rOAy\\\xa9\x92\x97zO\xe3\xd2C',
    b'\xdc\xea#\x04\x82\rD\xe4!P\xd4\x83E&\xcad\x0e\x12D\x8fE\x92\xc8\xa46\xd3\x1d\x12u\x82\xe1\x17',
    b"\xb1\xa9\xe9\\@\x0f]p\xd0\x89'y\xf4\xf6Fi\xc5\xcf\x99\x07\xf4yz\x13\x1f##\xb9\xec\xa8\xa2'",
    b'\xc6\xdc\x8a\x07d\x9e\xfb\xa4\xd8\xc5/Qc\xc2Yt\xfb\xdb\x96\xa1\x1a!\xce2M\xc6\xb4\x0b_\xbcp}',
    b'\xef\xdc\xf6\xc5\xde\xe5\x13o`\xa8\x9f\xce\x14\xc1n\x9d\xa4L\x8b\xcdK\nI\x12\x89\xaf\x1aq\xd3\x87\x8d\x06',
    b'\x06;\x17\xf26\xee\x1fC~\xa0\xc2\xca&t\xf2\xa3%$\x97\xc2\xce\x0fS\xb2R&\xba\xe3\xdf"\xefs',
    b'\xfb|$\x00\xe0W\xfb\xc6GY\xc5mh}of\x9bZ\x18\x86\xe8\xbb\x01Y\x14`\xfa\xc3\xd5\xe3Y\x7f',
    b'\x92\xcd\xf8\x86\xd7Q\xd6(V\xea\x92\x19\x852-\x91\xe9\x03\x194.\xb0\xba\xe8\xacb50\xa2Rs\x8c',
    b'\xd1\x16\x13\x8c\x14\x8f{\xc2\xcc\xe8\xe6\xf3\xa2x\x17\xd4\x06\x81\xa1C\x07\xdfp\xf4\x03e\x86\x02\xdfg"l',
    b'}\xcfm\x06\xe0\x11\x01y\xed\x19KI\x1c\xef\x8e\x86\x93\xf9\xe4\xee\xf9\xdcPF\x8f7\x05\xe9\xe6+S\xc6',
    b'\x88\xfd\xc9i3\xf7\xe4y\xbbO\x92\x97\xac\x87p\xdb4\xd8\xf1/i0\xa8\x16\x01i\x9d\x0cc\xe49\xaa',
    b'\x96\xae\xc7\xc7\xcca\xa3\x82\x98\xa3\xa6\xce0!\xf3\xae&\x80\xcd\xcbGac3\x0e\x9c\xd3J\xef\xf2\xc7~'
]
