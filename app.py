#!/usr/bin/env python3

from pytrex import PytrexHttp

if __name__ == '__main__':
    # httpserver.serve_forever()
    # pytrex_server = PytrexHttp.PytrexHttp()
    # pytrex_server.serve()
    
    # test for HTTPUtils
    # url = HTTPUtils.URLUtils()
    
    # httpserver = SocketConnection.HTTPConnection(('localhost', 8888))
    # httpserver.start_async_server()
    
    s = PytrexHttp.PytrexHttp(('localhost', 8888), 'asynchronous')
    s.serve_forever()




