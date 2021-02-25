import os
import sys

if len(sys.argv) != 2:
    sys.exit(1)

candidate = sys.argv[1]
dirs = os.listdir(candidate)
for dir in dirs:
    config = os.path.join(candidate, dir, "config.ini")
    result = os.path.join(candidate, dir)
    cmd = f"python __init__.py -c {config} -r {result} -d"
    os.system(cmd)
