"""
able to reconnect when server is down and back up
"""

import socket
import time
from threading import Thread


class ReconnectingClient(Thread):
    def __init__(self):
        self.running = True
        self.host = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket()
        self.port = 6000
        Thread.__init__(self)

    def run(self):
        while self.running:
            is_connection_ok = self.reconnect()
            if is_connection_ok:
                try:
                    self.sock.sendall('refresh'.encode())
                except ConnectionAbortedError:
                    print('connection aborted')
                    self.sock = self.close_and_reinit(self.sock)
                time.sleep(5)

        self.sock.close()

    @staticmethod
    def close_and_reinit(sock):
        sock.close()
        so = socket.socket()
        return so

    def reconnect(self):
        try:
            self.sock.connect((self.host, self.port))
            return True
        except ConnectionRefusedError as err:
            print('could not open connection')
            return False
        except OSError as err:
            if err.errno == 10056:
                print('connection is already open')
                return True
            else:
                print('connection is invalid')
                self.sock.close()
                return False


if __name__ == '__main__':
    reco_cli = ReconnectingClient()
    reco_cli.start()
