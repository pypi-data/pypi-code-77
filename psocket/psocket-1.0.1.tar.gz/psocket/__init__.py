import socket

from plogger import logger

logger = logger('SocketClient')


class SocketClient:
    """Create socket and establish connect to service using tuple host+port"""

    def __init__(self, host: str, port: int = 0, logger_enabled: bool = True):
        """Create and connect client to a remote host.

        :param host: Host IP
        :param port: Port
        :param logger_enabled: Enable/disable module logger
        """

        self.host = host
        self.port = port
        self.logger_enabled = logger_enabled

        # Initialize logger
        self.logger = logger

        try:
            self.client = socket.create_connection((self.host, self.port))
        except ConnectionRefusedError as err:
            self.logger.error(f'Cannot establish socket connection to {self.host}:{self.port}. {err}')
        except socket.gaierror as err:
            self.logger.error(f'Check host and port format. {self.host}:{self.port}. {err}')

    def __str__(self):
        return str(self._socket_response())

    def is_socket_available(self, port: int = 0, host: str = None, timeout: int = 5) -> bool:
        """Check remote socket is available.

        Port 0 used by default. Used port from construct is not specified.

        :param host:
        :param port:
        :param timeout:
        """

        host_ = host if host else self.host
        port_ = port if port else self.port

        try:
            with socket.create_connection((host_, port_), timeout=timeout) as sock:
                sock.settimeout(None)
                self.logger.info(f'[{host_}:{port_}] is available')
                return True
        except socket.timeout:
            self.logger.info(f'[{host_}:{port_}] unavailable')
            return False

    def wait_socket_available(self, port: int = 0, host: str = None, timeout: int = 5):
        """Wait for a socket availability

        :param port:
        :param host:
        :param timeout:
        :return:
        """

        timer = 0
        status = self.is_socket_available(port=port, host=host, timeout=timeout)

        while not status:
            status = self.is_socket_available(1)
            timer += 1

            if timer > timeout:
                raise TimeoutError(f'The service was not started within {timeout} seconds.')
        return status

    def _greeting(self):
        """Works only for the first connection in all project"""
        return self._socket_response()

    def send_command(self, cmd=''):
        command = self._encode_command(cmd)

        self.logger.info('COMMAND: ' + cmd)

        try:
            self.client.send(command)
            response = self._socket_response()
            self.logger.debug(response)

            return response
        except AttributeError as err:
            self.logger.error(err)
            # raise

    def _socket_response(self):
        data = self.client.recv(65536).decode()
        response = data.strip().split('\n')
        self.logger.debug('[RESPONSE]: ' + str(response))
        return response

    def close_connection(self):
        self.client.close()

    @staticmethod
    def _encode_command(cmd):
        return (cmd + '\n').encode()

    def get_sock_name(self) -> tuple:
        """Get local IP and port"""
        return self.client.getsockname()

    def get_peer_name(self) -> tuple:
        """Get remote IP and port"""
        return self.client.getpeername()
