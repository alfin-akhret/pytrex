#!/usr/bin/env python3
#
# Author: Alfin Akhret <alfin.akhre@gmail.com>
# 
# asynchronous.py
# Module ini terdiri dari class-class yang melakukan operasi Asynchronous I/O

import select

class Async():
    def all_events(self, poll_object):
        """ file descriptor and events generator """
        while True:
            for fd, event in poll_object.poll():
                yield fd, event

    