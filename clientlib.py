import socket,pickle
import threading
import json
import diffie_hellman
import crypto

HOST = '127.0.0.1'
PORT = 54005

class client:
    def __init__(self,port,homeFolder):
            self.port = port
            self.online = 0
            self.homeFolder=homeFolder
    def signin(self,name,pswd):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        cpy = self
        cpy.choice = 1
        cpy.pswd = pswd
        cpy.name = name
        s.send(pickle.dumps(cpy))
        if s.recv(1).decode()=="1":
            self.online = 1
            return 1
        else:
            return 0
        s.close()
    def signup(self,name,rollnum,pswd):
        self.name = name
        self.rollnum = rollnum
        self.pswd = pswd
        self.choice = -1
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        self.choice = 2
        s.sendall(pickle.dumps(self))
        if s.recv(1).decode()=="1":
            threading.Thread(target=self.listen).start()
            return 1
        else:
            return 0
        s.close()
    def listen(self):
        print('Server Started Listening....')
        host = '127.0.0.1'
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        server.bind((host,self.port))
        server.listen()
        while True:
            conn,addr=server.accept()
            print(addr)
            recvieved_message=bytearray()
            while True:
                temp_recvieved_message=conn.recv(1024)
                recvieved_message+=temp_recvieved_message
                if len(temp_recvieved_message)<1024:
                    break
            #have to add decryption
            if recvieved_message==b'DHKE':
                self.dhke=diffie_hellman.DiffieHellman(self.rollnum)
                #print("OBJ created")
                self.dhke.party2_key_exchange(conn)
                encrypted_message=bytearray()
                while True:
                    temp_encrypted_message=conn.recv(1024)
                    encrypted_message+=temp_encrypted_message
                    if len(temp_encrypted_message)<1024:
                        break
                #decrypt the message here
                encrypted_message=bytes(encrypted_message)
                decrypted_data=crypto.decrypt_p2p(encrypted_message,self.dhke.key1,self.dhke.key2,self.dhke.key3)
                data = json.loads(decrypted_data)
                if data['type']=='text':
                    print(data['msg'])
                else:
                    self.storeFile(conn,data['fileName'])
            
            conn.close()
    def storeFile(self,conn,fileName):
        f = open(self.homeFolder+'/'+fileName,'wb')
        while(True):
            data=conn.recv(1024)
            if not data:
                break
            decrypted_data=crypto.decrypt_p2p(data,self.dhke.key1,self.dhke.key2,self.dhke.key3)
            f.write(decrypted_data)
        f.close()
        print(fileName ," received")

    def sendFile(self,clientName,fileName):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        cpy = self
        cpy.choice = 3
        cpy.name = clientName
        s.sendall(pickle.dumps(cpy))
        port = pickle.loads(s.recv(1024)).port
        f = open(self.homeFolder +"/"+fileName,'rb')
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,port))
        self.dhke=diffie_hellman.DiffieHellman(self.rollnum)
        s.connect((HOST,port))
        self.dhke.initiate_key_exchange(s)
        messageObj = {}
        messageObj['type'] = 'file'
        messageObj['fileName'] = fileName
        s.send(pickle.dumps(messageObj))
        print(fileName ," sent")
        #changed size to 1023 so that encrypted result is 1024 bytes or less
        l = f.read(1023)
        while (l):
            cipher_text=crypto.encrypt_p2p(l,self.dhke.key1,self.dhke.key2,self.dhke.key3)
            s.send(cipher_text)
            l = f.read(1023)
        f.close()
        s.close()
    def message(self,name,msg):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        cpy = self
        cpy.choice = 3
        cpy.name = name
        s.sendall(pickle.dumps(cpy))
        port = pickle.loads(s.recv(1024)).port
        messageObj = {}
        messageObj['type'] = 'text'
        messageObj['msg']=msg
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.dhke1=diffie_hellman.DiffieHellman(self.rollnum)
        s.connect((HOST,port))
        self.dhke1.initiate_key_exchange(s)
        plain_text=json.dumps(messageObj).encode('utf-8')
        cipher_text=crypto.encrypt_p2p(plain_text,self.dhke1.key1,self.dhke1.key2,self.dhke1.key3)
        #s.send(pickle.dumps(messageObj))
        s.sendall(cipher_text)
        s.close()
    def join_group(self,name):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        cpy = self
        cpy.choice = 4
        cpy.groupname = name
        s.sendall(pickle.dumps(cpy))
        s.close()
    def list_group(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        cpy = self
        cpy.choice = 5
        s.sendall(pickle.dumps(cpy))
        groupstring = s.recv(1024).decode()
        s.close()
        return groupstring
    def mess_group(self,name,message):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        cpy = self
        cpy.choice = 6
        cpy.groupname=name
        cpy.msg = message
        s.sendall(pickle.dumps(cpy))
        s.close()
