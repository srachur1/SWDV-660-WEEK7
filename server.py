import socket                
from cryptography.fernet import Fernet

#Register the HostName with the CA server
def Register_with_CA(HostName):
    host = '127.0.0.1'
    port = 9500
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    #Generate public key
    public_key = Fernet.generate_key() 
    data= "server" + ',' + HostName + ',' + repr(public_key.decode()).strip("'")
    
    #send the server info to the CA server.  
    s.send(data.encode('utf-8'))
    ack = s.recv(1024)
    message = repr(ack.decode('utf-8','strict'))     
    print(message)
    s.close()
    return public_key

#start the server and accept client connections
def startServer(HostName, public_key):
    pk = public_key
    name = HostName
    s = socket.socket()          
    host = '127.0.0.1'
    port = 9600                
    s.bind((host, port))         
    s.listen(5)      
    print("Socket is listening on port ", port)     
    print("Web server is running...")         
    
    
    while True:
        
        conn, addr = s.accept()      
        print('Got connection from', addr)
        
        data_r = conn.recv(1024)

        if repr(data_r.decode('utf-8')).strip("'") == "What is the host name?":
            #Sends hostname to client.
            conn.send(name.encode('utf-8'))
            print('Sent name', name, 'to client. ')
        else: 
            f = Fernet(pk)
            message = f.decrypt(data_r)
            if message == b'session cipher key':
                print("Message received: " + repr(message.decode()))
                print("Sending client the acknowledgement...")
                msg = f.encrypt(b"session cipher key acknowledgement")
                conn.send(msg)  

             
            else:
                print("Goodbye")
                

def main():
    HostName = input("Enter the hostname to register with the CA server: ")
    public_key = Register_with_CA(HostName)
    startServer(HostName, public_key)

main()