import sys
import pathlib
abs = pathlib.Path(__file__).parent.absolute()
print(abs)
sys.path.insert(0, abs)

from helper import pip_install_or_ignore
from helper import log
import logging

pip_install_or_ignore("ipynb_path", "ipynb_path")
#pip_install_or_ignore("import_ipynb", "import_ipynb")
pip_install_or_ignore("websocket", "websocket-client")
pip_install_or_ignore("plotly", "plotly")
pip_install_or_ignore("simplejson", "simplejson")
pip_install_or_ignore("asyncio", "asyncio")
pip_install_or_ignore("grpc", "grpcio-tools")
pip_install_or_ignore("matplotlib", "matplotlib")
pip_install_or_ignore("autobahn", "autobahn")
pip_install_or_ignore("zlib", "zlib")
pip_install_or_ignore("pandas", "pandas")
pip_install_or_ignore("timeit", "timeit")
pip_install_or_ignore("dateutil", "python-dateutil")
pip_install_or_ignore("chipmunkdb", "chipmunkdb-python-client")
##pip_install_or_ignore("modin", "modin[ray]")
pip_install_or_ignore("raccoon", "raccoon")


global coinlib_job_task

from Registrar import Registrar
from Functions import Functions
from Features import Features
from Statistics import Statistics
from Simulator import Simulator

features = Features()
functions = Functions()
statistics = Statistics()
simulator = Simulator()
registrar = Registrar()

def debug(debug = True):
    if debug:
        log.basicConfig(level=logging.INFO)
    else:
        log.basicConfig(level=logging.ERROR)
    return None

def register(hostname):
    registrar.setBackendPath(hostname)
    ### lets reload all

def main():
    pass


