#! /usr/bin/env python3

import sys, os
import framedSocket
import myIO
import socket
from time import time
from threading import Thread, enumerate
import threading

threadNum = 0
inTransfer = set()
transferLock = threading.Lock()

class Worker(Thread):                       # for my threaded file transfer
    def __init__(self, conn, addr):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
        self.conn = conn                    # the connection properties
        self.addr = addr

    def checkTransfer(self, fileName):      # checks if a file is already in transfer
        global inTransfer
        global transferLock
        transferLock.acquire()              # acquires a lock on checking if a file is in use
        if fileName in inTransfer:
            canTransfer = False
        else:
            canTransfer = True
            inTransfer.add(fileName)
        transferLock.release()
        return canTransfer

    def endTransfer(self, fileName):        # removes the file from the files currently in transfer
        global inTransfer
        inTransfer.remove(fileName)

    def run(self):
        fs = framedSocket.SocketFramed(self.conn)        # new framed socket
        myIO.myPrint("Connected by: %s %d\n"%self.addr)  # prints the connection
        type1 = fs.recieveMessage()                 # recieves "Send", "Recv" later if needed
        filename = fs.recieveMessage()              # recieves the name of the file to be written
        canTransfer = self.checkTransfer(filename)
        if(canTransfer == False):
            fs.sendMessage(b"AW")
        elif os.path.isfile("./ServerFiles/"+filename): # checks if file already exists
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
            self.endTransfer(filename)
        self.conn.shutdown(socket.SHUT_WR)
