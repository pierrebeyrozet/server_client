import socket
import time

s = socket.socket()
host = socket.gethostbyname(socket.gethostname())
s.connect((host, 6000))
for i in range(12):
    s.sendall('refresh'.encode())
    time.sleep(5)

s.close()
