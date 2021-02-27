import os
from pyx import DEFAULT_TAG, render
from pyx import __APP__


tags_set = []
__pyx__ = lambda: ''
__PYX_FILE__ = os.environ.get("__PYX__") or '.'
try:
    exec(f'from {__PYX_FILE__} import *')
    exec(f'from {__PYX_FILE__} import __pyx__')
except ImportError as e:
    print(e)

__pyx__ = DEFAULT_TAG.update(name='pyx')(__pyx__)


rules = dict((r.rule, r.endpoint) for r in __APP__.url_map.iter_rules())

if '/' not in rules:
    @__APP__.route('/')
    def index():
        return render(__pyx__())
else:
    print(f'index route exists, using {rules["/"]} endpoint')

__APP__.run(debug=True)
