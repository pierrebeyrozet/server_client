import socket

s = socket.socket()
s.connect(('local_host', 6000))
s.sendall('her i am')
s.close()