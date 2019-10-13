import socket
from cryptography.fernet import Fernet

#Establish initial connection with the server to get the hostname
def ContactServer():
    host = '127.0.0.1'
    port = 9600
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    msg = "What is the host name?"
    s.send(msg.encode('utf-8'))
    data = s.recv(1024)
    name = repr(data.decode('utf-8')).strip("'")
    s.close()
    print("Got hostname from server: ", name)
    return name

#Contact the CA to verify the hostname 
def CheckHostName(name):
    host = '127.0.0.1'
    port = 9500
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    msg = "client" + "," + name
    s.send(msg.encode('utf-8'))
    
    data = s.recv(1024)
    public_key = repr(data.decode()).strip("'")
    s.close()
    return public_key

#Connect to the server 
def ConnectServer(public_key):
    host = '127.0.0.1'
    port = 9600
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    key = public_key.encode('utf-8')
    secret = b"session cipher key"
    f = Fernet(key)
    msg = f.encrypt(secret)
    s.send(msg)  
    data_r = s.recv(1024)
    print(data_r)
    message = f.decrypt(data_r)
    if message == b'session cipher key acknowledgement':
        print("Message received: " + repr(message.decode()))
        print("####################################")
    else:
        print("Goodbye")

    s.close()


def main():
    print("####################################")
    HostName = ContactServer()
    print("####################################")
    print("Contacting CA to verify Hostname")
    print("####################################")
    public_key = CheckHostName(HostName)
    print("Sending session cipher key to the server")
    print("####################################")
    ConnectServer(public_key)

main()
