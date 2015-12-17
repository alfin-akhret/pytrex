#!/usr/bin/env python3

from __future__ import absolute_import

from pytrex.TCPAsync import TCPListeningSocketHandler
from pytrex.TCPAsync import TCPConnectedSocketHandler
from pytrex.TCPAsync import event_loop
 

HOST, PORT, RECV_BUFFER = '', 8888, 1024
CONNECTION_LIST = []
backlog = 5

class HTTPServer(TCPConnectedSocketHandler):
    def is_readable(self):
        return True

    def do_read(self):
        data = self.connected_socket.recv(1024)
        if not data:
            self.close()
        else:
            self.outgoing.extend(data)

    
def serve_forever():
    handlers = []
    handlers.append(TCPListeningSocketHandler((HOST, PORT), HTTPServer, handlers))
    event_loop(handlers)
