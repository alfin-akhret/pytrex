#!/usr/bin/env python3
#
# Author: alfin.akhret@gmail.com

from __future__ import absolute_import

import select
from pytrex.low_level import TCPUtils
from pytrex.low_level import asynchronous

class PytrexHttp(TCPUtils.TCPConnection):
    
    def __init__(self):
        TCPUtils.TCPConnection.__init__(self, host='127.0.0.1', port=8888)
        self.async = asynchronous.Async()
        print('server is listening on locahost port 8888')

    def serve(self):
        # put listening socket into the 'sockets' list
        self.sockets[self.s.fileno()] = self.s
        # register listening socket ke poll_object
        self.async.register(self.s)

        # the main_loop
        for fd, event in self.async.all_events():
            # check the socket list, search socket with this fd number
            # and put it into sock variable to be processed later
            sock = self.sockets[fd]

            # if it's a new socket
            # it means its a connected socket from a client
            # put it in the list, register it to poll_object
            # and set its eventmask to POLLIN
            # done
            if sock is self.s:
                conn, address = sock.accept()
                self.sockets[conn.fileno()] = conn
                self.addresses[conn] = address
                self.async.register(conn)

            # if it's an event from already connected socket
            # and if it's a POLLIN event
            # means there's data ready to read on that fd, receive it
            elif event & select.POLLIN:
                more_data = sock.recv(2096) # TODO: this is the recv buffer, this should be defined in a constant or in separated conf file
                if not more_data:
                    sock.close()
                    continue
                # print(more_data)
                data = self.bytes_received.pop(sock, b'') + more_data
                # do the protocol routine here...
                if data.startswith(b'GET'):
                    # self.bytes_to_send[sock] = b'Ok...' + data
                    # trying to implement HTTP/1.0 response
                    content = b'''\

<html>
<head><title>Pytrex Home</title>
<body>
<p> Hi Client, I'm pytrex. Your friendly web framework</p>
</body>
</html>
'''
                    response = b'''\
HTTP/1.0 200 OK
Server: pytrex/0.0.1-dev
Content-Type: text/html
'''
                    response += content

                    self.bytes_to_send[sock] = b''+ bytearray(response)

                    self.async.modify(sock, "POLLOUT")
                else:
                    self.bytes_received[sock] = data

            # if there's event from connected sock
            # and it mask is POLLOUT
            # means there's data ready to send to client
            elif event & select.POLLOUT:
                data = self.bytes_to_send.pop(sock)
                n = sock.send(data)
                if n < len(data):
                    self.bytes_to_send[sock] = data[n:]
                else:
                    # self.async.modify(sock, select.POLLIN)
                    self.async.unregister(fd)
                    sock.close() # close connection
                    del self.sockets[fd]
            # if client disconnected
            elif event & (select.POLLERR | select.POLLNVAL | select.POLLHUP):
                # delete fd from poll_object
                # delete sock from socks
                self.async.unregister(fd)
                del self.sockets[fd]




