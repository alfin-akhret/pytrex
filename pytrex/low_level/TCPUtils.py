#!/usr/bin/env python3
# 
# Author: Alfin Akhret <alfin.akhret@gmail.com>
#
# TCPUtils.py
# Module ini terdiri dari class yang berhubungan langsung dengan low-level networking interface pada kernel OS
# ex: socket

import socket
import sys

# default options untuk koneksi TCP
# host Interface. default: mendengarkan pada semua interface yang tersedia.
# warning: jangan pernah gunakan default value ini pada implementasi karena beresiko pada sisi security.
# Opsi ini saya sediakan hanya sebagai fallback program jika lupa mengisi default HOST pada file konfigurasi
# dalam kenyataan nya opsi ini tidak akan pernah dipakai karena pada file konfigurasi sudah disertakan nilai default (127.0.0.1)
# kecuali user menghapus nilai default tersebut dan menggantinya dengan empty string.
HOST = ''
# default port=80 Karena sebagian implementasi pada framework ini akan menggunakan protokol HTTP               
PORT = 80
# default receive buffer untuk incoming data dari client
RECV_BUFFER = 1024
# default backlog/connection queue
BACKLOG = 64
# default socket address family saat ini hanya mensupport IPv4
ADDRESS_FAMILY = socket.AF_INET
# default socket type di set sebagai TCP socket
SOCKET_TYPE = socket.SOCK_STREAM

class TCPConnection():
    """ Class ini berguna untuk membuat koneksi TCP """
    def __init__(self,
        host=HOST,
        port=PORT,
        recv_buffer=RECV_BUFFER,
        backlog=BACKLOG,
        address_family=ADDRESS_FAMILY,
        socket_type=SOCKET_TYPE):

        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.backlog = backlog
        self.address_family = address_family
        self.socket_type = socket_type

        # properti berikut berguna jika ingin mengimplementasikan Event-Driven I/O atau Asynchronous server
        # socket list
        self.sockets = {}
        # bytes receive
        self.bytes_received = {}
        self.bytes_to_send = {}
        # connected addresses list
        self.addresses = {} 

        # create socket
        try:
            self.s = socket.socket(self.address_family, self.socket_type)
        except socket.error as msg:
            print('Error creating socket: %s' % msg)
            sys.exit(1)

        # set socket options
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket to host and port
        try:
            self.s.bind((self.host, self.port))
        except socket.error as msg:
            print('Error binding socket: %s' % msg)
            sys.exit(1)

        # listening
        self.s.listen(self.backlog)
