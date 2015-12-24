#!/usr/bin/env python3
# 
# Author: Alfin Akhret <alfin.akhret@gmail.com>
#
# TCPUtils.py
# Module ini terdiri dari class yang berhubungan langsung dengan low-level networking interface pada kernel OS
# ex: socket

import socket
import sys

# default options untuk koneksi TCP

class TCPConnection:
    """ Base TCP connection class """
    recv_buffer = 1024
    request_queue_size = 64
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, address, activate=True):
        """Constructor. Boleh di extend. Tapi jangan di override"""
        self.host = address[0]
        self.port = address[1]
        # properti berikut berguna jika ingin mengimplementasikan Event-Driven I/O atau Asynchronous server
        self.socket_list = {}
        self.bytes_received = {}
        self.bytes_to_send = {}
        self.addresses = {} 

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
            self.s.bind((self.host, self.port))
        except socket.error as msg:
            print('Error binding socket: %s' % msg)
            sys.exit(1)

    def listen(self):
        """dipanggil oleh constructor """
        self.s.listen(self.request_queue_size)

    def close(self):
        """close socket"""
        self.s.close()

    def serve(self):
        # must be implemented
        raise NotImplemented('This must be implemented')
