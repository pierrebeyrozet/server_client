import socket
import time
from threading import Thread


class ReconnectingServer(Thread):
    def __init__(self):
        self.sock = socket.socket()
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 6000
        self.running = True
        Thread.__init__(self)

        self.sock.bind((self.host, self.port))

    def run(self):
        self.sock.listen(5)
        c, addr = self.sock.accept()
        while self.running:
            print('got connection from ', addr)
            msg = c.recv(1024)
            print(msg)
            if not msg:
                print('lost connection to client')
                c.close()
                c, addr = self.sock.accept()
                time.sleep(1)

    # @staticmethod
    # def close_and_reinit(sock):
    #     sock.close()
    #     so = socket.socket()
    #     return so


if __name__ == '__main__':
    reco_srv = ReconnectingServer()
    reco_srv.start()
