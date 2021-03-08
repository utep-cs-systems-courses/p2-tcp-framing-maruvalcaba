# Manuel Ruvalcaba
# March 7, 2021
# Theory of Operating Systems
# Dr. Freudenthal
# This is the framed socket of a file transfer program.

class SocketFramed:
    def __init__(self, connectedSocket):
        self.cs = connectedSocket
        self.buff = ""
        
    def sendMessage(self, message):
        msglen = str(len(message))
        msg = msglen.encode()+b":"+message
        while len(msg):
            bytes = self.cs.send(msg)
            msg = msg[bytes:]

    def recieveMessage(self):
        if(self.buff == ""):
            self.buff += self.cs.recv(100).decode()
        lenMsg = ""
        for i in range(len(self.buff)):
            if self.buff[i] == ":":
                self.buff = self.buff[i+1:]
                break
            lenMsg += self.buff[i]
        if(lenMsg == ""):
            return ""
        intlenMsg = int(lenMsg)
        msg = ""
        while((len(msg) < intlenMsg)):
            msg += self.buff[0]
            if(len(self.buff) == 0):
                self.buff = self.cs.recv(100).decode()
            self.buff = self.buff[1:]
        return msg
