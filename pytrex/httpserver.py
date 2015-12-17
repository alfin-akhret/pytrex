#!/usr/bin/env python3

import socket
import sys
from _thread import *

HOST, PORT, RECV_BUFFER = '', 8888, 1024


class server(object):
    def __init__(self):        
        # create a socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print('Error creating socket: %s' % e)
            sys.exit(1)

        # set socket options
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as e:
            print('Error binding socket: %s' % e)
            sys.exit(1)

    def serv_forever(self, max_conn=1):
        self.socket.listen(max_conn)
        while True:
            client_conn, client_addr = self.socket.accept()
            print('A client connected from {}'.format(client_addr))
            start_new_thread(self.client_thread, (client_conn,))
        self.socket.close()

    def client_thread(self, client_conn):
        while True:
            # receive data from client
            try:
                buf = client_conn.recv(RECV_BUFFER)
            except socket.error as e:
                print('Error receiving data: %s' % e)
                sys.exit(1)
            if not len(buf):
                break
            resp = b'Ok...' + buf 
            client_conn.sendall(resp)
        client_conn.close()
