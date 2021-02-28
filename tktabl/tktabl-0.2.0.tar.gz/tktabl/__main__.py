import sys
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m tktable"

from . import _test as main
main()