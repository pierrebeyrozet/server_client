from multiprocessing.connection import Listener
from time import sleep

listener = Listener(('localhost', 6000), authkey=b'pwd1')
running = True
while running:
    conn = listener.accept()
    print('connection accepted from', listener.last_accepted)
    while True:
        msg = conn.recv()
        print(msg)
        if msg == 'close connection':
            conn.close()
            break
        if msg == 'close server':
            conn.close()
            running = False
            break
    sleep(1)
listener.close()