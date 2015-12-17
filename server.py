#!/usr/bin/env python3

import socket
import sys

HOST, PORT, RECV_BUFFER = '', 8888, 1024

# create socket object
# make it listen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

print('server is listening on {host}:{port}...'.format(host=s.getsockname()[0], port=str(s.getsockname()[1])))

# listen for new incoming connection
while True:
    client_conn, client_addr = s.accept()
    print('A client connected from {}'.format(client_addr))
    # receive incoming message from client
    message = client_conn.recv(RECV_BUFFER)
    # send response
    resp = b'OK...' + message
    client_conn.sendall(resp)
    # close connected socket
    client_conn.close()

# close listening socket
s.close()
   

