import random
import socket   
from cryptography.fernet import Fernet

#Start the CA Server
def startCA():
    s = socket.socket()          
    host = '127.0.0.1'
    port = 9500                
    s.bind((host, port))         
    s.listen(5)      
    print("Socket is listening on port ", port)         
    print("CA Server is running...")      
    
    while True:
        conn, addr = s.accept()      
        print('Got connection from', addr)
        data_r = conn.recv(1024)
        data = repr(data_r.decode()).strip("'").split(',')
        
        if data[0] == "server":
            f= open("registry.txt", "r")
            for lines in f:
                if data[1] in lines:
                    f.close()
                    print("Server is already registered")
                    break
            else:
                f= open("registry.txt","a")
                f.write("\n" + data[1] + ',' + data[2])
                f.close()

            msg = "Server Name is registered."
            conn.send(msg.encode('utf-8'))

         
        else:
            f= open("registry.txt", "r")
            for lines in f:
                if data[1] in lines:
                    reg = lines.strip().split(',')
                    msg = reg[1]
                    f.close()
                    break
            else:
                msg = Fernet.generate_key()
            
        
        conn.send(msg.encode('utf-8'))

    conn.close() 


startCA()
