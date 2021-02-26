#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zlib
import sys


if __name__ == "__main__":
    infile = sys.stdin.buffer
    content = infile.read()
    text = zlib.decompress(content)
    try:
        text = text.decode('utf8', errors="ignore")
    except Exception as e:
        print("I can only handler utf8 text now")
    print(text)
