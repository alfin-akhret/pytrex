#!/usr/bin/env python3
# 
# Author: Alfin Akhret <alfin.akhret@gmail.com>
#
# SocketConnection.py
# Module ini terdiri dari class yang berhubungan langsung dengan low-level networking interface pada kernel OS
# ex: socket
from __future__ import absolute_import

import socket
import sys
from functools import wraps
from pytrex.low_level import AsynchronousUtils

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
        self.async = AsynchronousUtils.Async()
        self.socket_list = {}
        self.addresses = {}
        self.bytes_received = {}
        self.bytes_to_send = {}

    def start_async_server(self):
        self.socket_list[self.fileno()] = self.s
        self.async.register(self.s)

        for fd, event, eventmask in self.async.all_events():
            sock = self.socket_list[fd]

            if sock == self.s:
                # handle incoming new connection here
                self.accept_new_conn()

            elif event & eventmask.POLLIN:
                # handle readble socket here
                more_data = self.receive_data(sock)
                if not more_data:
                    sock.close()
                    continue
                data = self.bytes_received.pop(sock, b'') + more_data
                if self.is_http_request(data):
                    # compose response
                    response = b'[Server] OK...\n' # TODO: craft response using HTTP implementation module
                    self.bytes_to_send[sock] = response
                    self.async.modify(sock, "POLLOUT")
                else:
                    self.bytes_received[sock] = data

            elif event & eventmask.POLLOUT:
                # handle writeable socket here
                data = self.bytes_to_send.pop(sock)
                n = sock.send(data)
                if n < len(data):
                    self.bytes_to_send[sock] = data[n:]
                else:
                    self.async.unregister(fd)
                    sock.close() # close connection
                    del self.socket_list[fd]
        
            elif event & (eventmask.POLLERR | eventmask.POLLNVAL | eventmask.POLLHUP):
                # handle socket error here
                self.async.unregister(fd)
                del self.socket_list[fd]
    
    # override TCPConnection.accept_new_conn() method
    def accept_new_conn(self):
        conn = super(HTTPConnection, self).accept_new_conn()
        self.socket_list[conn[0].fileno()] = conn[0]
        self.addresses[conn[0]] = conn[1]
        self.async.register(conn[0])

    # simple HTTP wrapper
    # TODO: this sould be written in seperate modules exclusively to implements HTTP protocol
    def check_request(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            retval = func(*args, **kwargs)
            if retval.startswith('GET'):
                return True
            else:
                return False
        return func_wrapper

    @check_request
    def is_http_request(self, data_buffer):
        return data_buffer

   
        

    

