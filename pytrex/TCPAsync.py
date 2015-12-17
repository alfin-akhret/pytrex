#!/usr/bin/env python3
#
# Author: alfin.akhret@gmail.com

""" Asynchrounous TCP base classes """

import socket
import select
import sys

class EventHandler:
    """ This is the Abstract class for creating
        TCP EventHandler class """

    def fileno(self):
        # return the file descriptor
        raise NotImplemented('Must implement')

    def is_readable(self):
        # return True if the descriptor is readable
        # means if receiving is allowed
        return False

    def do_read(self):
        # perform read operation
        pass

    def is_writeable(self):
        # return True if the descriptor is writeable
        # means if sending is allowed
        return False

    def do_write(self):
        # perform write operation
        pass

def event_loop(handlers):
    while True:
        read_handler = [h for h in handlers if h.is_readable()]
        write_handler = [h for h in handlers if h.is_writeable()]
        readable, writeable, _ = select.select(read_handler, write_handler, [])
        for h in readable:
            h.do_read()
        for h in writeable:
            h.do_write()


class TCPServerHandler(EventHandler):
    """ Base class for any TCP connection
        its primary role is related to the TCP 'listeniing socket'
        which is to create a listening socket and 
        add incoming connection (connected socket) file descriptor
        to the handler_list"""
        
    def __init__(self, address, tcp_client_handler, handler_list):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except OSError as e:
            print('Error creating socket: %s' % e)
            self.s = None
            sys.exit(1)

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.s.bind(address)
        except OSError as e:
            print('Error binding socket.', e)
            self.s = None
            sys.exit(1)

        self.s.listen(1)

        self.tcp_client_handler = tcp_client_handler
        self.handler_list = handler_list

    def fileno(self):
        return self.s.fileno()

    def is_readable(self):
        return True

    def do_read(self):
        client_conn, client_address = self.s.accept()
        self.handler_list.append(self.tcp_client_handler(client_conn, self.handler_list))

class TCPClientHandler(EventHandler):
    """ TCP Client handler is a base class
        dealing with TCP 'connected socket' """
    
    def __init__(self, client_socket, handler_list):
        self.client_socket = client_socket
        self.handler_list = handler_list
        self.outgoing = bytearray()

    def fileno(self):
        return self.client_socket.fileno()

    def is_writeable(self):
        return True if self.outgoing else False

    def do_write(self):
        buf = self.client_socket.send(self.outgoing)
        self.outgoing = self.outgoing[buf:]


# TESTING CODE:
# sample implementation of TCPClientHandler
# TODO: to the future, this can be HTTP handler, SSH Handler, etc
class ExampleHTTPHandler(TCPClientHandler):
    def is_readable(self):
        return True

    def do_read(self):
        data = self.client_socket.recv(1024)
        if not data:
            self.close()
        else:
            self.outgoing.extend(data)

if  __name__ == '__main__':
    handlers = []
    handlers.append(TCPServerHandler(('',8888), ExampleHTTPHandler, handlers))
    event_loop(handlers)
