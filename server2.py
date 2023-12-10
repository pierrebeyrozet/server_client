from multiprocessing.connection import Listener

listener = Listener(('localhost', 6001), authkey=b'pwd2')
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