import socket

s = socket.socket()
host = socket.gethostbyname(socket.gethostname())
s.bind((host, 6000))

s.listen(5)
running = True
c, addr = s.accept()
while running:
    print('got connection from ', addr)
    msg = c.recv(1024)
    print(msg)
    if not msg:
        break

c.close()
