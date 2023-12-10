from multiprocessing.connection import Listener

listener = Listener(('localhost', 6002), authkey=b'pwd3')
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
listener.close()