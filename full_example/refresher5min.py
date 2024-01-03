import socket
import time
from threading import Thread
from queue import Queue

STRATS = {'STRAT_1': {'port': 7000, 'tframes': (5,)},
          'STRAT_2': {'port': 7001, 'tframes': (15,)}
          }

# refresher has a server thread that receives the messages from ingester
# refresher has n client threads to send message to strats
# refresher sends only the info that the strat subscribe to (for example LCOG4 30min)


class Refresher:
    def __init__(self, refresher_port):
        self.host = socket.gethostbyname(socket.gethostname())
        self.server = ReconnectingServer(self.host, 6000)
        self.running = True
        self.freq = 5
        self.queues = dict()

        self.init_queues()

    def init_queues(self):
        for key in STRATS.keys():
            self.queues[key] = Queue()

    def start_work(self):
        self.server.start()


class ReconnectingServer(Thread):
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.host = host
        self.port = port
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
            else:

                a = 0





# s = socket.socket()
# host = socket.gethostbyname(socket.gethostname())
# s.bind((host, 6000))
#
# s.listen(5)
# running = True
# c, addr = s.accept()
# while running:
#     print('got connection from ', addr)
#     msg = c.recv(1024)
#     print(msg)
#     if not msg:
#         break
#
# c.close()
