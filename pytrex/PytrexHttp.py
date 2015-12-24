#!/usr/bin/env python3
#
# Author: alfin.akhret@gmail.com

from __future__ import absolute_import

from pytrex.low_level import SocketConnection
from pytrex.low_level import asynchronous

class PytrexHttp(SocketConnection.HTTPConnection):

    host = '127.0.0.1'
    port = 8888

    def __init__(self):
        SocketConnection.HTTPConnection.__init__(self,  (self.host, self.port))
        self.async = asynchronous.Async()
        print('server is listening on locahost port {0}'.format(str(self.port)))

    def serve(self):
        # put listening socket into the 'sockets' list
        self.socket_list[self.s.fileno()] = self.s
        # register listening socket ke poll_object
        self.async.register(self.s)

        # the main_loop
        for fd, event, em in self.async.all_events():
            # check the socket list, search socket with this fd number
            # and put it into sock variable to be processed later
            sock = self.socket_list[fd]

            # if it's a new socket
            # it means its a connected socket from a client
            # put it in the list, register it to poll_object
            # and set its eventmask to POLLIN
            # done
            if sock is self.s:
                conn, address = sock.accept()
                self.socket_list[conn.fileno()] = conn
                self.addresses[conn] = address
                self.async.register(conn)

            # if it's an event from already connected socket
            # and if it's a POLLIN event
            # means there's data ready to read on that fd, receive it
            elif event & em.POLLIN:
                more_data = sock.recv(self.recv_buffer) 
                if not more_data:
                    sock.close()
                    continue
                # print(more_data)
                data = self.bytes_received.pop(sock, b'') + more_data
                # do the protocol routine here...
                if data.startswith(b'GET'):
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
            elif event & em.POLLOUT:
                data = self.bytes_to_send.pop(sock)
                n = sock.send(data)
                if n < len(data):
                    self.bytes_to_send[sock] = data[n:]
                else:
                    self.async.unregister(fd)
                    sock.close() # close connection
                    del self.socket_list[fd]

            # if client disconnected
            elif event & (em.POLLERR | em.POLLNVAL | em.POLLHUP):
                # delete fd from poll_object
                # delete sock from socks
                self.async.unregister(fd)
                del self.socket_list[fd]




