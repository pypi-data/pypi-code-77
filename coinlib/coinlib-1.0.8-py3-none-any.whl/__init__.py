import sys

import importlib
from coinlib.helper import in_ipynb, set_loglevel
from coinlib.helper import pip_install_or_ignore
import subprocess
from coinlib.helper import log
import logging
import sys

pip_install_or_ignore("ipynb_path", "ipynb_path")
# pip_install_or_ignore("import_ipynb", "import_ipynb")
pip_install_or_ignore("websocket", "websocket-client")
pip_install_or_ignore("plotly", "plotly")
pip_install_or_ignore("simplejson", "simplejson")
pip_install_or_ignore("asyncio", "asyncio")
pip_install_or_ignore("grpc", "grpcio-tools")
pip_install_or_ignore("matplotlib", "matplotlib")
pip_install_or_ignore("zlib", "zlib")
pip_install_or_ignore("pandas", "pandas")
pip_install_or_ignore("timeit", "timeit")
pip_install_or_ignore("dateutil", "python-dateutil")
pip_install_or_ignore("chipmunkdb", "chipmunkdb-python-client")

global coinlib_job_task

from coinlib.Registrar import Registrar
from coinlib.Functions import Functions
from coinlib.Features import Features
from coinlib.Statistics import Statistics
from coinlib.Simulator import Simulator
from coinlib.ChartsIndicatorJob import ChartsIndicatorJob

def debug(self, debug=True):
    if debug:
        log.basicConfig(level=logging.INFO)
    else:
        log.basicConfig(level=logging.ERROR)
    return None

registrar = Registrar()
features = Features()
functions = Functions()
statistics = Statistics()
simulator = Simulator()
pip_install_or_ignore = pip_install_or_ignore
set_loglevel = set_loglevel

def connect(self, hostname):
    registrar.setBackendPath(hostname)

    ### lets reload all

