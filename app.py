#!/usr/bin/env python3

from pytrex import PytrexHttp

if __name__ == '__main__':
    # httpserver.serve_forever()
    pytrex_server = PytrexHttp.PytrexHttp()
    pytrex_server.serve()