
def sendMessage(socket, message):
    msglen = str(len(message))
    msg = msglen.encode()+b":"+message
    while len(msg):
        bytes = socket.send(msg)
        msg = msg[bytes:]

buffer = ""
        
def recieveMessage(socket):
    global buffer
    buffer += socket.recv(100).decode()
    lenMsg = ""
    for i in range(len(buffer)):
        if buffer[i] == ":":
            buffer = buffer[i+1:]
            break
        lenMsg += buffer[i]
    if(lenMsg == ""):
        return ""
    intlenMsg = int(lenMsg)
    msg = ""
    while((len(msg) < intlenMsg)):
        msg += buffer[0]
        if(len(buffer) == 1):
            buffer = socket.recv(100).decode()
        buffer = buffer[1:]
    return msg
