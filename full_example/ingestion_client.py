import socket
import time
from threading import Thread
from queue import Queue

REFRESHERS = {'RFSHR_5': 6000,
              'RFSHR_15': 6001}


class BarIngester:
    def __init__(self, refreshers_dict):
        self.host = socket.gethostbyname(socket.gethostname())
        self.running = True
        self.refreshers_conn = self.create_connections_and_queues(refreshers_dict)
        self.freq = 5

    @staticmethod
    def create_connections_and_queues(refresher_dict):
        cli = dict()
        for name, port in refresher_dict.items():
            cli[name] = ReconnectingClient(socket.gethostbyname(socket.gethostname()),
                                           port)
        return cli

    def start_connection_threads(self):
        for name in self.refreshers_conn.keys():
            self.refreshers_conn[name].start()

    def run(self):
        self.start_connection_threads()
        while self.running:
            self.send_messages('refresh')
            time.sleep(self.freq)

    def send_messages(self, msg):
        for name in self.refreshers_conn.keys():
            if self.refreshers_conn[name].is_conn_ok:
                self.refreshers_conn[name].queue.put(msg)


class ReconnectingClient(Thread):
    def __init__(self, host, port):
        self.running = True
        self.host = host
        self.sock = socket.socket()
        self.port = port
        self.queue = Queue()
        Thread.__init__(self)
        self.is_conn_ok = False

    def run(self):
        while self.running:
            self.is_conn_ok = self.reconnect()
            if self.is_conn_ok:
                msg = self.queue.get()
                try:
                    self.sock.sendall(msg.encode())
                except ConnectionAbortedError:
                    print('connection aborted')
                    self.sock = self.close_and_reinit(self.sock)

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
    bi = BarIngester(REFRESHERS)
    bi.run()