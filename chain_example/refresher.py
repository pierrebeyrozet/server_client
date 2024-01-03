from threading import Thread
import socket
from queue import Queue


class MyServer(Thread):
    def __init__(self, shared_queue: Queue = None):
        self.shared_queue = shared_queue
        Thread.__init__(self)

    def run(self):
        s = socket.socket()
        host = socket.gethostbyname(socket.gethostname())
        s.bind((host, 6000))

        s.listen(5)
        c, addr = s.accept()
        print('got connection from ', addr)
        running = True
        while running:
            print('receiving data from ingestion')
            message = c.recv(1024)
            msg = message.decode('utf-8')
            if msg == 'refresh':
                data = self.get_data()
                self.shared_queue.put(data)
            elif msg == 'stop':
                running = False
        c.close()

    @staticmethod
    def get_data():
        return 'this is some data'


class MyClient(Thread):
    def __init__(self, shared_queue: Queue = None):
        self.shared_queue = shared_queue
        Thread.__init__(self)

    def run(self):
        s = socket.socket()
        s.connect((socket.gethostbyname(socket.gethostname()), 7000))
        running = True
        while running:
            data = self.shared_queue.get()
            print('sending data to strat')
            s.sendall(data.encode())

        s.close()


class Refresher:
    def __init__(self):
        self.shared_queue = Queue()
        self.cli = MyClient(self.shared_queue)  # downstream process
        self.srv = MyServer(self.shared_queue)  # upstream process

    def start_work(self):
        self.cli.start()
        self.srv.start()


if __name__ == '__main__':
    rfshr = Refresher()
    rfshr.start_work()