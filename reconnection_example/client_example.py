import socket
import time

s = socket.socket()
host = socket.gethostbyname(socket.gethostname())
s.connect((host, 6000))
for i in range(500):
    s.sendall(f'refresh {i}'.encode())
    time.sleep(5)

s.close()