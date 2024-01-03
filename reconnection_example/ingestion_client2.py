import socket
import time
from threading import Thread


class MyClient(Thread):
    def __init__(self):
        self.sock = socket.socket()
        self.host = socket.gethostbyname(socket.gethostname())
        self.conn_ok = False
        Thread.__init__(self)

    def connection_handler(self):
        try:
            self.sock.connect((self.host, 6000))
            self.conn_ok = True
        except ConnectionRefusedError:
            print('could not open connection')
            self.conn_ok = False
        except OSError:
            print('connection is already open')
            self.conn_ok = True

    def run(self):
        running = True
        while running:
            self.connection_handler()
            # if is_connection_ok:
                # try:
                #     self.sock.sendall('refresh'.encode())
                # except ConnectionAbortedError:
                #     print('connection aborted')
                #     self.sock.close()
            time.sleep(15)

        self.sock.close()

    def send_message(self, payload):
        self.sock.sendall(payload.encode())


class MyWorker:
    def __init__(self):
        self.cli = MyClient()

    def do_stuff(self):
        running = True
        while running:
            if self.cli.conn_ok:
                self.cli.send_message('refresh')
            time.sleep(5)

    def start_connections(self):
        self.cli.start()


if __name__ == '__main__':
    wrkr = MyWorker()
    wrkr.start_connections()
    wrkr.do_stuff()