import curses
import os
import GLXCurses
import time


class FileChooserUtils(object):
    FILE_HIGH_LIGHT = {
        "executable": {"type": "FILE_EXE"},
        "directory": {"type": "DIR"},
        "device": {"type": "DEVICE"},
        "special": {"type": "SPECIAL"},
        "stalelink": {"type": "STALE_LINK"},
        "symlink": {"type": "SYMLINK"},
        "hardlink": {"type": "HARDLINK"},
        "core": {"regexp": "^core\\.*\\d*$", "extensions_case": True},
        "temp": {"extensions": "~", "regexp": "(^"},
        "archive": {
            "color": (170, 0, 170),
            "attributes": curses.A_BOLD,
            "extensions": [
                "7z",
                "Z",
                "ace",
                "arc",
                "arj",
                "ark",
                "bz2",
                "cab",
                "gz",
                "lha",
                "lz",
                "lz4",
                "lzh",
                "lzma",
                "rar",
                "rpm",
                "tar",
                "tbz",
                "tbz2",
                "tgz",
                "tlz",
                "txz",
                "tzst",
                "xz",
                "zip",
                "zoo",
                "zst",
            ]
        },
        "doc": {
            "color": (255, 199, 6),
            "attributes": curses.A_NORMAL,
            "extensions": [
                "chm",
                "css",
                "ctl",
                "diz",
                "doc",
                "docm",
                "docx",
                "dtd",
                "htm",
                "html",
                "letter",
                "lsm",
                "mail",
                "man",
                "me",
                "msg",
                "nroff",
                "odp",
                "ods",
                "odt",
                "pdf",
                "po",
                "ppt",
                "pptm",
                "pptx",
                "ps",
                "rtf",
                "sgml",
                "shtml",
                "tex",
                "text",
                "txt",
                "xls",
                "xlsm",
                "xlsx",
                "xml",
                "xsd",
                "xslt",
            ]
        },
        "source": {
            "color": (0, 170, 170),
            "attributes": curses.A_NORMAL,
            "extensions": [
                "ada",
                "asm",
                "awk",
                "bash",
                "c",
                "caml",
                "cc",
                "cgi",
                "cpp",
                "cxx",
                "diff",
                "erl",
                "h",
                "hh",
                "hi",
                "hpp",
                "hs",
                "inc",
                "jasm",
                "jav",
                "java",
                "js",
                "m4",
                "mak",
                "mjs",
                "ml",
                "mli",
                "mll",
                "mlp",
                "mly",
                "pas",
                "patch",
                "php",
                "phps",
                "pl",
                "pm",
                "prg",
                "py",
                "rb",
                "sas",
                "sh",
                "sl",
                "st",
                "tcl",
                "tk",
                "xq",
            ]
        },
        "media": {
            "color": (57, 181, 74),
            "attributes": curses.A_NORMAL,
            "extensions": [
                "3gp",
                "aac",
                "ac3",
                "ape",
                "asf",
                "avi",
                "dts",
                "flac",
                "flv",
                "it",
                "m3u",
                "m4a",
                "med",
                "mid",
                "midi",
                "mkv",
                "mod",
                "mol",
                "mov",
                "mp2",
                "mp3",
                "mp4",
                "mpeg",
                "mpg",
                "mpl",
                "ogg",
                "ogv",
                "s3m",
                "umx",
                "vob",
                "wav",
                "webm",
                "wma",
                "wmv",
                "xm",
            ]
        },
        "graph": {
            "color": (0, 170, 170),
            "attributes": curses.A_BOLD,
            "extensions": [
                "ai",
                "bmp",
                "cdr",
                "eps",
                "gif",
                "ico",
                "jpeg",
                "jpg",
                "omf",
                "pcx",
                "pic",
                "png",
                "rle",
                "svg",
                "tif",
                "tiff",
                "webp",
                "wmf",
                "xbm",
                "xcf",
                "xpm",
            ]
        },
        "database": {
            "color": (180, 180, 180),
            "attributes": curses.A_NORMAL,
            "extensions": [
                "cdx",
                "dat",
                "db",
                "dbf",
                "dbi",
                "dbx",
                "fox",
                "mdb",
                "mdn",
                "mdx",
                "msql",
                "mssql",
                "pgsql",
                "sql",
                "ssql",
            ]
        },
    }

    # FILE_HIGH_LIGHT_PREP = {'7z': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'Z': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'ace': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'arc': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'arj': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'ark': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'bz2': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'cab': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'gz': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'lha': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'lz': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'lz4': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'lzh': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'lzma': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'rar': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'rpm': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'tar': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'tbz': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'tbz2': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'tgz': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'tlz': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'txz': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'tzst': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'xz': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'zip': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'zoo': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'zst': {'attributes': 0, 'color': (170, 0, 170), 'category': 'archive'},
    #                         'chm': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'css': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'ctl': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'diz': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'doc': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'docm': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'docx': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'dtd': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'htm': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'html': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'letter': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'lsm': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'mail': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'man': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'me': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'msg': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'nroff': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'odp': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'ods': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'odt': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'pdf': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'po': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'ppt': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'pptm': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'pptx': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'ps': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'rtf': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'sgml': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'shtml': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'tex': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'text': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'txt': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'xls': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'xlsm': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'xlsx': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'xml': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'xsd': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'xslt': {'attributes': 0, 'color': (255, 199, 6), 'category': 'doc'},
    #                         'ada': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'asm': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'awk': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'bash': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'c': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'caml': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'cc': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'cgi': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'cpp': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'cxx': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'diff': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'erl': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'h': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'hh': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'hi': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'hpp': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'hs': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'inc': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'jasm': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'jav': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'java': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'js': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'm4': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'mak': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'mjs': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'ml': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'mli': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'mll': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'mlp': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'mly': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'pas': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'patch': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'php': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'phps': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'pl': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'pm': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'prg': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'py': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'rb': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'sas': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'sh': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'sl': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'st': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'tcl': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'tk': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         'xq': {'attributes': 0, 'color': (0, 170, 170), 'category': 'source'},
    #                         '3gp': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'aac': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'ac3': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'ape': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'asf': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'avi': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'dts': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'flac': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'flv': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'it': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'm3u': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'm4a': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'med': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mid': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'midi': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mkv': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mod': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mol': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mov': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mp2': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mp3': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mp4': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mpeg': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mpg': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'mpl': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'ogg': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'ogv': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         's3m': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'umx': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'vob': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'wav': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'webm': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'wma': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'wmv': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'xm': {'attributes': 0, 'color': (57, 181, 74), 'category': 'media'},
    #                         'ai': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'bmp': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'cdr': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'eps': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'gif': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'ico': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'jpeg': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'jpg': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'omf': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'pcx': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'pic': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'png': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'rle': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'svg': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'tif': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'tiff': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'webp': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'wmf': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'xbm': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'xcf': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'xpm': {'attributes': 0, 'color': (180, 180, 180), 'category': 'graph'},
    #                         'cdx': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'dat': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'db': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'dbf': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'dbi': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'dbx': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'fox': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'mdb': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'mdn': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'mdx': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'msql': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'mssql': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'pgsql': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'sql': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'},
    #                         'ssql': {'attributes': 0, 'color': (180, 180, 180), 'category': 'database'}}

    FILE_HIGH_LIGHT_PREP = {}
    for category in ['archive', 'doc', 'source', 'media', 'graph', 'database']:
        for extension in FILE_HIGH_LIGHT[category]["extensions"]:
            FILE_HIGH_LIGHT_PREP[".{0}".format(extension)] = {
                "attributes": FILE_HIGH_LIGHT[category]["attributes"],
                "color": FILE_HIGH_LIGHT[category]["color"],
                "category": category,
            }

    def __init__(self):
        self.__cwd = None
        self.__sort_by_name = None
        self.__sort_name_order = None
        self.__sort_by_size = None
        self.__sort_size_order = None
        self.__sort_by_mtime = None
        self.__sort_mtime_order = None
        self.__directory_view = None

        self.cwd = None
        self.sort_by_name = True
        self.sort_name_order = True
        self.sort_by_size = False
        self.sort_size_order = True
        self.sort_by_mtime = False
        self.sort_mtime_order = True
        self.directory_view = None
        self.app_file_extensions = None

    @property
    def directory_view(self):
        """
        The directory view property is use to store the result of a scan directory.

        :return: The view of the current directory as a list
        :rtype: list of dict
        :raise TypeError: When property value us not a list type or None
        """
        return self.__directory_view

    @directory_view.setter
    def directory_view(self, value=None):
        """
        Set the ``directory_view`` property value

        :param value: `directory_view`` property value to set
        :type value: list
        """
        if value is None:
            value = []
        if type(value) != list:
            raise TypeError(
                "'directory_view' property value must be a list Type or None"
            )
        if self.directory_view != value:
            self.__directory_view = value

    @property
    def cwd(self):
        """
        The ``cwd`` property store the location of the current directory value

        If set to ``None`` it return os.getcwd() value

        :return: The current working directory value
        :rtype: str
        :raise TypeError: When property value is not a str type or None
        :raise ValueError: When property value is not a valid directory
        """
        return self.__cwd

    @cwd.setter
    def cwd(self, value=None):
        """
        Set the ``cwd`` property value

        :param value: The directory path to store o rNone for default Value ``os.getcwd()``
        :return:
        """
        if value is None:
            value = os.getcwd()
        if type(value) != str:
            raise TypeError("'cwd' property value must be a str Type or None")
        if not os.path.isdir(os.path.realpath(value)):
            raise ValueError("'cwd' property value must be a real directory")
        if self.cwd != value:
            self.__cwd = os.path.realpath(value)

    @property
    def sort_by_name(self):
        """
        Return sort_by_name attribute.

        :return: True if enable, False if disable
        :rtype: bool
        """
        return self.__sort_by_name

    @sort_by_name.setter
    def sort_by_name(self, boolean=True):
        """
        Set the sort_name_order attribute . It use for display files and directory sorted by name in order.

        Order are:
            True for A to Z
            False for Z to A

        :param boolean: True for A to Z, False for Z to A
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type or None
        """
        if boolean is None:
            boolean = False
        if boolean is not None and type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type")
        if self.sort_by_name != boolean:
            self.__sort_by_name = boolean

    @property
    def sort_name_order(self):
        """
        Return sort_name_order attribute.

        :return: True if ordering A to Z, False if ordering Z to A
        :rtype: bool
        """
        return self.__sort_name_order

    @sort_name_order.setter
    def sort_name_order(self, boolean=True):
        """
        Set the sort_name_order attribute . It use for display files and directory sorted by name in order.

        Order are:
            True for A to Z
            False for Z to A

        :param boolean: True for A to Z, False for Z to A
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type or None")
        if self.sort_name_order != boolean:
            self.__sort_name_order = boolean

    @property
    def sort_by_size(self):
        """
        Return sort_by_size attribute.

        :return: True if enable, False if disable
        :rtype: bool
        """
        return self.__sort_by_size

    @sort_by_size.setter
    def sort_by_size(self, boolean=None):
        """
        Set the sort_by_size attribute . It use for display files and directory sorted by size.

        :param boolean: True for enable, False for disable
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type")

        # just in case we make the job
        if self.sort_by_size != boolean:
            self.__sort_by_size = boolean

    @property
    def sort_size_order(self):
        """
        Return sort_by_size attribute. as set by set_sort_size_order()

        :return: True if enable, False if disable
        :rtype: bool
        """
        return self.__sort_size_order

    @sort_size_order.setter
    def sort_size_order(self, boolean=None):
        """
        Set the sort_size_order attribute . It use for display files and directory sorted by size in order.

        Order are:
            True: Min to Max
            False: Max to Min

        :param boolean: True if ordering Min to Max, False if ordering Max to Min.
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type")
        if self.sort_size_order != boolean:
            self.__sort_size_order = boolean

    @property
    def sort_by_mtime(self):
        """
        Return sort_by_mtime attribute.

        :return: True if enable, False if disable
        :rtype: bool
        """
        return self.__sort_by_mtime

    @sort_by_mtime.setter
    def sort_by_mtime(self, boolean=None):
        """
        Set the sort_by_mtime attribute . It use for display files and directory sorted by mtime.

        :param boolean: True for enable, False for disable
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type or None")
        if self.sort_by_mtime != boolean:
            self.__sort_by_mtime = boolean

    @property
    def sort_mtime_order(self):
        """
        Return sort_mtime_order attribute. as set by set_sort_mtime_order()

        :return: True if ordering Now to Ago, False if ordering Ago to Now.
        :rtype: bool
        """
        return self.__sort_mtime_order

    @sort_mtime_order.setter
    def sort_mtime_order(self, boolean=True):
        """
        Set the sort_size_order attribute . It use for display files and directory sorted by mtime in order.

        Order are:
            True: Now to Ago
            False: Ago to Now

        :param boolean: True if ordering Now to Ago, False if ordering Ago to Now.
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type or None
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type or None")
        if self.sort_mtime_order != boolean:
            self.__sort_mtime_order = boolean

    def __scan(self, directory):
        # Brutally create the data structure
        list_file = []
        list_dir = []
        # noinspection PyUnresolvedReferences
        for item in [
            {
                "name": item.name,
                "path": os.path.join(self.cwd, item.name),
                "directory": self.cwd,
                "is_dir": item.is_dir(),
                "is_file": item.is_file(),
                "is_exec": item.is_file() and os.access(os.path.join(self.cwd, item.name), os.X_OK),
                "is_symlink": item.is_symlink(),
                "st_mtime": item.stat(follow_symlinks=False).st_mtime,
                "st_size": item.stat(follow_symlinks=False).st_size,
                "to_display_name": item.name,
                "to_display_size": GLXCurses.sizeof(item.stat(follow_symlinks=False).st_size),
                "to_display_mtime": time.strftime(
                    "%d/%m/%Y  %H:%M", time.localtime(item.stat(follow_symlinks=False).st_mtime)
                ),
                "to_display_symbol": " ",
                "to_display_color": (255, 255, 255),
                "to_display_attributes": curses.A_NORMAL,
            }
            for item in directory
        ]:
            if item["is_dir"]:
                list_dir.append(item)

            elif item["is_file"]:
                list_file.append(item)

            elif item["is_symlink"]:
                list_file.append(item)

        return [list_dir, list_file]

    def __check_orders(self, lists):
        # list_file = lists[1]
        # list_dir = lists[0]
        if self.sort_by_name:

            lists[1].sort(key=lambda x: x["name"])
            lists[0].sort(key=lambda x: x["name"])

            if not self.sort_name_order:
                lists[1] = list(reversed(lists[1]))
                lists[0] = list(reversed(lists[0]))

        elif self.sort_by_size:

            lists[1].sort(key=lambda x: x["st_size"])
            lists[0].sort(key=lambda x: x["st_size"])

            if not self.sort_size_order:
                lists[1] = list(reversed(lists[1]))
                lists[0] = list(reversed(lists[0]))

        elif self.sort_by_mtime:
            lists[1].sort(key=lambda x: x["st_mtime"])
            lists[0].sort(key=lambda x: x["st_mtime"])

            if not self.sort_mtime_order:
                lists[1] = list(reversed(lists[1]))
                lists[0] = list(reversed(lists[0]))

        return lists[0] + lists[1]

    def __check_attributes(self, items):
        # Clean up
        for item in items:
            if item["is_file"]:
                if item["is_symlink"]:
                    item["to_display_symbol"] = "@"
                    item["to_display_color"] = self.get_infos_by_filename(filename=item["name"],
                                                                          key='color',
                                                                          default=(180, 180, 180)
                                                                          )
                    item["to_display_attributes"] = self.get_infos_by_filename(filename=item["name"],
                                                                               key='attributes',
                                                                               default=curses.A_NORMAL
                                                                               )

                    item['to_display_name'] = "-> {0}".format(os.readlink(item["path"]))
                else:
                    if item["is_exec"]:
                        item["to_display_symbol"] = "*"
                        item["to_display_color"] = (0, 255, 0)
                        item["to_display_attributes"] = curses.A_BOLD
                    else:
                        item["to_display_color"] = self.get_infos_by_filename(filename=item["name"],
                                                                              key='color',
                                                                              default=(180, 180, 180)
                                                                              )
                        item["to_display_attributes"] = self.get_infos_by_filename(filename=item["name"],
                                                                                   key='attributes',
                                                                                   default=curses.A_NORMAL
                                                                                   )

                    item['to_display_name'] = "{0}{1}".format(item["to_display_symbol"], item["name"])

            elif item["is_dir"]:
                if item["is_symlink"]:
                    if not os.path.exists(item["path"]):
                        item["to_display_symbol"] = "!"
                        item["to_display_color"] = (255, 0, 0)
                        item["to_display_attributes"] = curses.A_BOLD
                    else:
                        item["to_display_symbol"] = "~"
                        item["to_display_attributes"] = curses.A_BOLD

                    item['to_display_name'] = "-> {0}".format(os.readlink(item["path"]))

                else:
                    item["to_display_symbol"] = "/"
                    item['to_display_name'] = "{0}{1}".format(item["to_display_symbol"], item["name"])
                    item["to_display_color"] = (255, 255, 255)
                    item["to_display_attributes"] = curses.A_BOLD

            elif item["is_symlink"]:
                if not os.path.exists(item["path"]):
                    item["to_display_symbol"] = "!"
                    item["to_display_color"] = (255, 0, 0)
                    item["to_display_attributes"] = curses.A_BOLD

                item['to_display_name'] = "-> {0}".format(os.readlink(item["path"]))
        return items

    def __finalize(self, items):
        two_dot_path = os.path.join(self.cwd, "..")
        two_dot_info = os.stat(two_dot_path)
        items.insert(
            0,
            {
                "name": "..",
                "path": two_dot_path,
                "directory": self.cwd,
                "is_dir": True,
                "is_file": False,
                "is_symlink": False,
                "is_exec": False,
                "st_mtime": two_dot_info.st_mtime,
                "st_size": two_dot_info.st_size,
                "to_display_name": "UP--DIR",
                "to_display_size": "UP--DIR",
                "to_display_mtime": time.strftime(
                    "%d/%m/%Y  %H:%M", time.localtime(two_dot_info.st_mtime)
                ),
                "to_display_symbol": "/",
                "to_display_color": (180, 180, 180),
                "to_display_attributes": curses.A_NORMAL,
            },
        )
        return items

    def update_directory_list(self):
        try:
            self.directory_view = self.__finalize(
                self.__check_attributes(
                    self.__check_orders(
                        self.__scan(
                            os.scandir(self.cwd)
                        )
                    )
                )
            )
        except PermissionError:
            pass

    def set_app_file_extensions(self, file_extensions=None):
        """
        A tuple of file extension to colorize, it's consider as file type you searching for.

        The FileChooser will colorize they file's, in orange.

        Note the function automatically deal with case sensitive.

        Example: .mkv -> ('.mkv','.Mkv','MKV')

        :param file_extensions: a tuple of file extension to colorize or None for disable the colorize.
        :type file_extensions: tuple or None
        :raise TypeError: when ``file_extensions`` argument is not a tuple type or None
        """
        if file_extensions is None:
            if self.get_app_file_extensions() is not None:
                self.app_file_extensions = None
                return

        # Exit as soon of possible
        if type(file_extensions) != tuple:
            raise TypeError("'file_extensions' must be a tuple type")

        # Create a Tuple with Upper Lower and Title extension
        # Example: .mkv -> ('.mkv','.Mkv','MKV')
        file_extensions_temp = list()
        # Lower -> .mkv
        for item in list(file_extensions):
            file_extensions_temp.append(item.lower())
        # Title -> Mkv
        for item in list(file_extensions):
            file_extensions_temp.append(item.title())
        # Upper -> .MKV
        for item in list(file_extensions):
            file_extensions_temp.append(item.upper())
        video_file_extensions = tuple(file_extensions_temp)

        if self.get_app_file_extensions() != video_file_extensions:
            self.app_file_extensions = video_file_extensions

    def get_app_file_extensions(self):
        """
        Return the list of file extension to colorize.

        See . Filechooser.set_app_file_extensions() for more details.

        :return: a tuple of file extension to colorize or None if disable.
        :rtype: tuple or None
        """
        return self.app_file_extensions

    def get_color_by_filename(self, filename=None):
        if os.path.splitext(filename)[1] in self.FILE_HIGH_LIGHT_PREP:
            return self.FILE_HIGH_LIGHT_PREP[str(os.path.splitext(filename)[1])]['color']
        else:
            return 180, 180, 180

    def get_attributes_by_filename(self, filename=None, key=None, default=None):
        if os.path.splitext(filename)[1] in self.FILE_HIGH_LIGHT_PREP:
            return self.FILE_HIGH_LIGHT_PREP[str(os.path.splitext(filename)[1])][key]
        else:
            return curses.A_NORMAL

    def get_infos_by_filename(self, filename=None, key=None, default=None):
        if os.path.splitext(filename)[1] in self.FILE_HIGH_LIGHT_PREP:
            return self.FILE_HIGH_LIGHT_PREP[str(os.path.splitext(filename)[1])][key]
        else:
            return default

    def convert_file_attribute(self):
        dict_to_return = {}
        for category in ['archive', 'doc', 'source', 'media', 'graph', 'database']:
            for extension in self.FILE_HIGH_LIGHT[category]["extensions"]:
                # print(extension)
                dict_to_return[extension] = {
                    "attributes": self.FILE_HIGH_LIGHT[category]["attributes"],
                    "color": self.FILE_HIGH_LIGHT[category]["color"],
                    "category": category,
                }

        return dict_to_return
