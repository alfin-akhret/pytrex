#!/usr/bin/env python3
#
# Author: Alfin Akhret <alfin.akhret@gmail.com>
# Implementation of HTTP/1.0 and HTTP/1.1

class HTTPUtils():
    def __init__(self):
        pass

    def check_host_header(self, request_header):
        """Host header is required in HTTP/1.1
        Any request that came without it will get '400 Bad request' response"""
        pass

    def check_http_version(self, request_header):
        """There's a difference between HTTP/1.0 and HTTP/1.1
        Therefore we should check the request before doing other operation"""
        pass

    def check_URL(self, request_header):
        """Future implementation of HTTP (HTTP/1.2) will accept absoluth path
        instead of a pathname. We must support this transition"""
        pass








