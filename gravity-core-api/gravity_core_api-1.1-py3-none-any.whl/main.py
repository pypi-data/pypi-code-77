""" Перспективный единый TCP API endpoint для Gravity core """
from witapi.main import WITServer


class GCSE(WITServer):
    """ Gravity Core Single Endpoint """

    def __init__(self, myip, myport, sqlshell, gravity_engine, debug=False):
        super().__init__(myip, myport, sqlshell=sqlshell, without_auth=True, mark_disconnect=False, debug=debug)
        self.gravity_engine = gravity_engine

    def execute_command(self, comm, values):
        if comm == 'wserver_sql_command':
            response = self.sqlshell.try_execute(values['command'])
            print('Response:', response)
        return response
