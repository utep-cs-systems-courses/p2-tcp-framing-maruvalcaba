#! /usr/bin/env python3

import sys, os
import framedSocket
import myIO
import socket
from time import time
from threading import Thread, enumerate

threadNum = 0

class Worker(Thread):
    def __init__(self, conn, addr):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
        self.conn = conn
        self.addr = addr
    def run(self):
        fs = framedSocket.SocketFramed(self.conn)        # new framed socket
        myIO.myPrint("Connected by: %s %d\n"%self.addr)  # prints the connection
        type1 = fs.recieveMessage()                 # recieves "Send", "Recv" later if needed
        filename = fs.recieveMessage()              # recieves the name of the file to be written
        if os.path.isfile("./ServerFiles/"+filename): # checks if file already exists
            fs.sendMessage(b"NO")
        else:
            fs.sendMessage(b"OK")
            try:                                    # tries to write to the file
                fd = os.open("./ServerFiles/"+filename, os.O_CREAT | os.O_WRONLY)
                os.write(fd, fs.recieveMessage().encode())
                os.close(fd)
                fs.sendMessage(b"SUCCESS")          # success if successful
            except:
                fs.sendMessage(b"FAILURE WRITING FILE")
        self.conn.shutdown(socket.SHUT_WR)
