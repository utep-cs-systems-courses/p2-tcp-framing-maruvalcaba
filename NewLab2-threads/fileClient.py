#! /usr/bin/env python3

# Manuel Ruvalcaba
# March 7, 2021
# Theory of Operating Systems
# Dr. Freudenthal
# This is the client side of a file transfer program.

import socket, sys, re, time, os
sys.path.append("../lib")       # for params
import params
import framedSocket
import myIO
'''
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-i', '--inputf'), 'inputf', "text.txt"),
    (('-o', '--outputf'), 'outputf', "text.txt"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )
'''
progname = "fileClient"
#paramMap = params.parseParams(switchesVarDefaults)

#server, usage, inputf, outputf  = paramMap["server"], paramMap["usage"], paramMap["inputf"], paramMap["outputf"]

#if usage:
 #   params.usage()


try:                            # tries to get the necessary parameters
    clientFile = sys.argv[1]        
    serverHost, serverFile = re.split(":", sys.argv[2])
    serverPort = 50001
except:                         # if it fails, prints syntax.
    myIO.myPrint("Bad param format: '%s'. Should be $ ./fileClient Send {clientFile} {host:serverFile}\n" % sys.argv)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        myIO.myPrint("creating sock: af=%d, type=%d, proto=%d\n" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        myIO.myPrint(" error: %s\n" % msg)
        s = None
        continue
    try:
        myIO.myPrint(" attempting to connect to %s\n" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        myIO.myPrint(" error: %s\n" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    myIO.myPrint('could not open socket\n')
    sys.exit(1)
'''
delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")
'''
fs = framedSocket.SocketFramed(s)                # new framed socket
fs.sendMessage(sys.argv[0].encode())             # sent the mode, "Send", "Recv" later if needed
fs.sendMessage(serverFile.encode())              # sent the file name to be saved on server side
response = fs.recieveMessage()                   # gets response from the server, "OK" or "NO"
if(response == "OK"):
    message = myIO.myReadFile(clientFile)        # reads the contents of the client side file
    fs.sendMessage(message.encode())             # sends it to the server in the framed send
    result = fs.recieveMessage()                 # recieves a result of the transfer
    myIO.myPrint(result+"\n")                    # prints result, "SUCCESS" or "FAILURE WRITING FILE"
elif(response == "NO"):
    myIO.myPrint("File name already exists!\n")  # response was "NO"
else:
    myIO.myPrint("File currently being written to!\n")
s.close()
