import socket

s = socket.socket()
s.bind(('local_host', 6000))

s.listen(5)
while True:
    c, addr = s.accept()
    print('got connection from ', addr)
    print (c.recv(1024))
    c.close()