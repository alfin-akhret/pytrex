#!/usr/bin/env python3

from pytrex import httpserver

if __name__ == '__main__':
    s = httpserver.server()
    s.serv_forever()

