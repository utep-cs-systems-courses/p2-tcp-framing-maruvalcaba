#! /usr/bin/env python3

# Manuel Ruvalcaba
# March 7, 2021
# Theory of Operating Systems
# Dr. Freudenthal
# This is the server side of a file transfer program.

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
import framedSocket
import myIO

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        fs = framedSocket.SocketFramed(conn)
        myIO.myPrint("Connected by: %s %d\n"%addr)
        type1 = fs.recieveMessage()
        filename = fs.recieveMessage()
        if os.path.isfile("./ServerFiles/"+filename):
            fs.sendMessage(b"NO")
        else:
            fs.sendMessage(b"OK")
            try:
                fd = os.open("./ServerFiles/"+filename, os.O_CREAT | os.O_WRONLY)
                os.write(fd, fs.recieveMessage().encode())
                os.close(fd)
                fs.sendMessage(b"SUCCESS")
            except:
                fs.sendMessage(b"FAILURE WRITING FILE")
        conn.shutdown(socket.SHUT_WR)


