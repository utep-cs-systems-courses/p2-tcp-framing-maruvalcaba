# Manuel Ruvalcaba
# March 7, 2021
# Theory of Operating Systems
# Dr. Freudenthal
# This is the framed socket of a file transfer program.

class SocketFramed:
    def __init__(self, connectedSocket):  # to make a new framed socket
        self.cs = connectedSocket
        self.buff = ""
        
    def sendMessage(self, message):           # sends a out-of-band framed message
        msglen = str(len(message))
        msg = msglen.encode()+b":"+message
        while len(msg):
            bytes = self.cs.send(msg)
            msg = msg[bytes:]

    def recieveMessage(self):                # recieves a framed message, and returns the entire message to the recipient
        if(self.buff == ""):
            self.buff += self.cs.recv(100).decode() # if there is nothing in the buffer, it will recieve
        lenMsg = ""
        while(True):          # this for loop gets the message length
            if len(self.buff) == 0:
                self.buff = self.cs.recv(100).decode()
            if self.buff[0] == ":":
                self.buff = self.buff[1:]
                break
            lenMsg += self.buff[0]
            self.buff = self.buff[1:]
        if(lenMsg == ""):                        
            return ""
        intlenMsg = int(lenMsg)
        msg = ""
        while((len(msg) < intlenMsg)):           # while the length of the built msg is less than the length in the framing
            if(len(self.buff) == 0):             # if there is nothing left in the buff, read.
                self.buff = self.cs.recv(100).decode()
            msg += self.buff[0]
            self.buff = self.buff[1:]
        return msg
