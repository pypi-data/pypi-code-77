from helper import is_in_ipynb
from helper import pip_install_or_ignore
pip_install_or_ignore("ipynb_path", "ipynb_path")
pip_install_or_ignore("websocket", "websocket-client")
pip_install_or_ignore("plotly", "plotly")
pip_install_or_ignore("simplejson", "simplejson")
pip_install_or_ignore("asyncio", "asyncio")
pip_install_or_ignore("grpc", "grpcio-tools")
pip_install_or_ignore("matplotlib", "matplotlib")
pip_install_or_ignore("pandas", "pandas")
pip_install_or_ignore("timeit", "timeit")
pip_install_or_ignore("dateutil", "python-dateutil")
pip_install_or_ignore("chipmunkdb", "chipmunkdb-python-client")

import StatisticsMethodLoader
import StatisticsRuleLoader
import ChartsLoader
from DataWorker import WorkerJobListener
from Registrar import Registrar
import asyncio
from helper import log

registrar = Registrar()

def run_main_function():
    registrar.statsRuleFactory = StatisticsRuleLoader.StatisticsRuleFactory()
    registrar.statsMethodFactory = StatisticsMethodLoader.StatisticsMethodFactory()
    registrar.chartsFactory = ChartsLoader.ChartsFactory()

    workerJobs = WorkerJobListener()
    workerJobs.start()

    log.info("Starting Coinlib Factory")

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    run_main_function()
elif is_in_ipynb:
    run_main_function()