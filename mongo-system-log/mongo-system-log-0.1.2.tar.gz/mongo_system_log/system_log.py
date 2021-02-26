import logging
import inspect
from socket import socket, AF_INET, SOCK_DGRAM, gethostname
from datetime import datetime
from .mongodb_connector import ConnectMongo
from sys import argv


def configure_logs():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s ', level=logging.INFO)


def get_module_name():
    """This function gets module and file name that called it. Must be called on instantiate the LogThis class."""
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    return mod.__name__, argv[0]


class LogThis:

    def __init__(self, module):
        self.hostname = LogThis.get_hostname()
        self.ip = LogThis.get_host_ip()
        self.module = module[0]
        self.app = module[1]
        self.default_fields = {
            'Ip': self.ip,
            'HostName': self.hostname,
            'ModuleCalled': self.module,
            'App': self.app
        }

    def info(self, msg, payload=None, result=None, log_console=True, log_detail=True):

        log_id = self._send_mongo('info', msg=msg, payload=payload, result=result)

        if not log_id:
            return None

        if not log_console:
            return log_id

        if log_detail:
            logging.info(f'log_id:{log_id}, Message:{msg}, Module:{self.module}, App:{self.app}, '
                         f'Payload:{payload}, Result:{result}')
        else:
            logging.info(f'log_id:{log_id}, Message:{msg}')

        return log_id

    def error(self, msg, payload=None, result=None, log_console=True, log_detail=True):
        log_id = self._send_mongo('error', msg=msg, payload=payload, result=result)
        if not log_id:
            return None

        if not log_console:
            return log_id

        if log_detail:
            logging.error(f'log_id:{log_id}, Message:{msg}, Module:{self.module}, App:{self.app}, '
                          f'Payload:{payload}, Result:{result}')
        else:
            logging.error(f'log_id:{log_id}, Message:{msg}')

        return log_id

    def critical(self, msg, payload=None, result=None, log_console=True, log_detail=True):
        log_id = self._send_mongo('critical', msg=msg, payload=payload, result=result)
        if not log_id:
            return None

        if not log_console:
            return log_id

        if log_detail:
            logging.critical(f'log_id:{log_id}, Message:{msg}, Module:{self.module}, App:{self.app}, '
                             f'Payload:{payload}, Result:{result}')
        else:
            logging.critical(f'log_id:{log_id}, Message:{msg}')

        return log_id

    def _send_mongo(self, severity, msg, payload, result):
        _msg = {
            'Date': datetime.now(),
            'Severity': severity.upper(),
            'Message': msg,
            'Payload': payload,
            'Result': result
        }
        _msg.update(self.default_fields)
        try:
            mongodb_connection = ConnectMongo()
            log_id = mongodb_connection.db[severity].insert_one(_msg).inserted_id

            return log_id
        except Exception as e:
            _msg['Severity'] = 'CRITICAL'
            logging.critical(f'Fail to send log for MongoDb - {e}, Message:{_msg}')
            return None

    @staticmethod
    def get_hostname():
        try:
            host_name = gethostname()
        except:
            logging.error('Fail to get Hostname')
            host_name = 'N/A'
        return host_name

    @staticmethod
    def get_host_ip():
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            host_ip = s.getsockname()[0]
            s.close()
        except:
            logging.error('Fail to get get Ip')
            host_ip = 'N/A'
        return host_ip



