#!/usr/bin/env python3
# 
# Author: Alfin Akhret <alfin.akhret@gmail.com>
#
# SocketConnection.py
# Module ini terdiri dari class yang berhubungan langsung dengan low-level networking interface pada kernel OS
# ex: socket

import socket
import sys

# default options untuk koneksi TCP

class TCPConnection(object):
    """ Base TCP connection class """
    recv_buffer = 1024
    request_queue_size = 64
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, host_address, activate=True):
        """Constructor. Boleh di extend. Tapi jangan di override"""
        self.host_address = host_address
        if activate:
            self.bind()
            self.listen()

    def bind(self):
        """Dipanggil oleh consturctor untuk nge-bind socket"""
        # create socket
        try:
            self.s = socket.socket(self.address_family, self.socket_type)
        except socket.error as msg:
            print('Error creating socket: %s' % msg)
        
        # set socket options
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket to host and port
        try:
            self.s.bind(self.host_address)
        except socket.error as msg:
            print('Error binding socket: %s' % msg)
            sys.exit(1)

    def fileno(self):
        return self.s.fileno()

    def listen(self):
        """dipanggil oleh constructor """
        self.s.listen(self.request_queue_size)

    def close(self):
        """close socket"""
        self.s.close()

    def accept_new_conn(self):
        conn, addr = self.s.accept()
        return conn, addr

    def receive_data(self, connected_socket):
        return connected_socket.recv(self.recv_buffer)
        
    def send_data(self, connected_socket, data_buffer):
        return connected_socket.send(data_buffer)

    def serve(self):
        # must be implemented
        raise NotImplemented('This must be implemented')

class HTTPConnection(TCPConnection):
    """Base class for HTTP connection"""
    def __init__(self, host_address):
        """Constructor. Bisa di extends tapi jangan di override"""
        TCPConnection.__init__(self, host_address, True)
        self.socket_list = {}
        # self.bytes_received = {}
        # self.bytes_to_send = {}
        # self.addresses = {}

    def serve(self, poll_loop): 
        """ Main loop. Bisa diextends ataupun di override. Tapi harus diimplementasikan."""
        # while True:
        #     conn = self.accept_new_conn()
        #     print('Accepted connection from {}'.format(conn[1]))
        #     try:
        #         while True:
        #             # handle request here
        #             br = self.receive_data(conn[0])
        #             self.send_data(conn[0], br)
        #             conn[0].close()
        #             break
        #     except:
        #         raise
        self.socket_list[self.fileno()] = self.s
        
    def async(self, poll_loop):
        for fd, event, eventmask in poll_loop():
            sock = self.socket_list[fd]
            if sock == self.s:
                # handle new connection here
            elif event & eventmask.POLLIN:
                # a connected socket is readable
            elif event & eventmask.POLLOUT:
                # a connected socket is writeable
            else:
                # handle socket connection error here
    
    def send_data(self, data_buffer):
        """ override TCPConnection send_data methods """
        pass