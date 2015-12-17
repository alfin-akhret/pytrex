#!/usr/bin/env python3

import socket
import select
import sys
from _thread import *

HOST, PORT, RECV_BUFFER = '', 8888, 1024
CONNECTION_LIST = []
backlog = 5


class server(object):
    def __init__(self, backlog = 5):        
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

    def serv_forever(self):
        self.socket.listen(backlog)
        CONNECTION_LIST.append(self.socket)
        while True:
            try:
                readable, writeable, exceptional = select.select(CONNECTION_LIST, [],[])
            except select.error as e:
                break

            for sock in readable:
                # if readable socket is the listening socket
                # it means a new client is trying to connect
                # handle it
                if sock == self.socket:
                    client_conn, client_addr = self.socket.accept()
                    # add new connected client to the list
                    CONNECTION_LIST.append(client_conn)
                    print('A client connected from {}'.format(client_addr))
                else:
                    # handle already connected clients
                    try:
                        buf = sock.recv(RECV_BUFFER)
                    except socket.error as e:
                        print('Error receiving data %s' % e)
                        sys.exit(1)
                    if not len(buf):
                        break
                    resp = b'Ok...' + buf
                    try:
                        sock.sendall(resp)
                    except socket.error as e:
                        print('Error sending data %s' % e)
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                        continue

        self.socket.close()

    
