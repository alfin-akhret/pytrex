#!/usr/bin/env python3

import socket
import sys
from _thread import *

HOST, PORT, RECV_BUFFER = '', 8888, 1024

# create socket object
# make it listen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
   
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Socket binding failed. Error code:{err_code}. Error message:{err_msg}'.format(err_code=str(msg[0]), err_msg=str(msg[1])))
    sys.exit()

s.listen(1)
print('server is listening on {host}:{port}...'.format(host=s.getsockname()[0], port=str(s.getsockname()[1])))

# client thread
# use to maintain connection with connected client
# using threaded-server technique
def client_thread(client_conn):
    while True:
        data = client_conn.recv(RECV_BUFFER)
        if not data:
            break
        resp = b'Ok...' + data
        client_conn.sendall(resp)
    cleint_conn.close()

# listen for new incoming connection
while True:
    client_conn, client_addr = s.accept()
    print('A client connected from {}'.format(client_addr))
    start_new_thread(client_thread, (client_conn,))

# close listening socket
s.close()
   

