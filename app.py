#!/usr/bin/env python3

from pytrex.low_level import SocketConnection

if __name__ == '__main__':
    # httpserver.serve_forever()
    # pytrex_server = PytrexHttp.PytrexHttp()
    # pytrex_server.serve()
    
    # test for HTTPUtils
    # url = HTTPUtils.URLUtils()
    
    httpserver = SocketConnection.HTTPConnection(('localhost', 8888))
    httpserver.start_async_server()




