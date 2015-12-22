#!/usr/bin/env python3

from pytrex import httpserver
from pytrex import PytrexHttp
from pytrex.low_level import TCPUtils

if __name__ == '__main__':
    # httpserver.serve_forever()
    # pytrex_server = PytrexHttp.PytrexHttp()
    # pytrex_server.serve()
    
    tcp_server = TCPUtils.TCPConnection(host='127.0.0.1')