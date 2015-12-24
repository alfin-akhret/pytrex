#!/usr/bin/env python3
#
# Author: Alfin Akhret <alfin.akhre@gmail.com>
# 
# asynchronous.py
# Module ini terdiri dari class-class yang melakukan operasi Asynchronous I/O

import select

class Async():
    def __init__(self):
        self.poll_object = select.poll()

    def register(self, socket):
        # socket baru secara otomatis di beri eventmask POLLIN
        self.poll_object.register(socket, select.POLLIN)

    def modify(self, socket, eventmask='POLLOUT'):
        if eventmask is None or eventmask == 'POLLOUT':
            self.poll_object.modify(socket, select.POLLOUT)
        elif eventmask == 'POLLIN':
            self.poll_object.modify(socket, select.POLLIN)

    def unregister(self, fd):
        self.poll_object.unregister(fd)


    def all_events(self):
        """ file descriptor and events generator """
        while True:
            for fd, event in self.poll_object.poll():
                yield fd, event, select

    