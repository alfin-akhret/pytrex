#!/usr/bin/env python3

import socket
import sys
from _thread import *

HOST, PORT, RECV_BUFFER = '', 8888, 1024


class server(object):
    def __init__(self):        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((HOST, PORT))
        except socket.error as msg:
            print('Socket binding failed. Error code:{err_code}. Error message:{err_msg}'.format(err_code=str(msg[0]), err_msg=str(msg[1])))
            sys.exit()
        print('Socket created')

    def serv_forever(self, max_conn=1):
        self.socket.listen(max_conn)
        while True:
            client_conn, client_addr = self.socket.accept()
            print('A client connected from {}'.format(client_addr))
            start_new_thread(self.client_thread, (client_conn,))
        self.socket.close()

    def client_thread(self, client_conn):
        while True:
            data = client_conn.recv(RECV_BUFFER)
            if not data:
                break
            resp = b'Ok...' + data
            client_conn.sendall(resp)
        client_conn.close()
