#!/usr/bin/env python3
#
# Author: alfin.akhret@gmail.com

from __future__ import absolute_import

from pytrex.low_level import SocketConnection

class PytrexHttp(SocketConnection.HTTPConnection):
    def __init__(self, host_address, server_type='asynchronous'):
        self.server_type = server_type
        SocketConnection.HTTPConnection.__init__(self, host_address)

    def serve_forever(self):
        if self.server_type == 'asynchronous':
            self.start_async_server()