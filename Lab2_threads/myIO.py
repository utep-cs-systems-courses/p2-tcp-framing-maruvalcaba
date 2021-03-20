# Manuel Ruvalcaba
# March 7, 2021
# Theory of Operating Systems
# Dr. Freudenthal
# This is the IO of a file transfer program.

import os

def myPrint(message):
    os.write(1, message.encode())


def myReadFile(filename):
    fd = os.open("./ClientFiles/"+filename, os.O_RDONLY)
    next = 0
    limit = 0
    sbuf = ""
    ibuf = ""
    message = ""
    while 1:
        ibuf = os.read(fd, 100)
        sbuf = ibuf.decode()
        limit = len(sbuf)
        if limit == 0:
            break
        message += sbuf
    return message
