import socket,pickle
import threading
import json
import diffie_hellman
import crypto
import time
HOST = '127.0.0.1'
PORT = 54005

class client:
    def __init__(self,port,homeFolder):
            self.port = port
            self.online = 0
            self.homeFolder=homeFolder
            self.grouplist={}

    def signin(self,name,pswd):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        requestObj = {}
        requestObj['choice'] = 'signin'
        requestObj['pswd'] = pswd
        requestObj['name'] = name
        s.sendall(pickle.dumps(requestObj))
        if s.recv(1).decode()=="1":
            self.online = 1
            s.close()
            return 1
        else:
            s.close()
            return 0

    def signup(self,name,rollnum,pswd):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        requestObj = {}
        requestObj['choice'] = 'signup'
        requestObj['roll-num'] = rollnum
        requestObj['pswd'] = pswd
        requestObj['port']=self.port
        requestObj['name'] = name
        self.name=name
        self.password=pswd
        self.rollnum=rollnum
        s.sendall(pickle.dumps(requestObj))
        if s.recv(1).decode()=="1":
            threading.Thread(target=self.listen).start()
            s.close()
            return 1
        else:
            s.close()
            return 0

    def listen(self):
        print('Server Started Listening....')
        host = '127.0.0.1'
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        server.bind((host,self.port))
        server.listen()
        while True:
            conn,addr=server.accept()
            #print(addr)
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
                #print(data)
                if data['type']=='text':
                    print(data['sender'],':',data['msg'])
                else:
                    self.storeFile(conn,data,False,data['sender'])
            else:                       
                data = pickle.loads(recvieved_message)
                #print(data)
                if data['type']=='text':
                    decrypted_data = crypto.decrypt_group_message(data['encrypted'],self.grouplist[data['groupname']])
                    print("Group Message :"+data['groupname'])
                    print(decrypted_data.decode())
                else:
                    self.storeFile(conn,data,True)
            conn.close()

    def storeFile(self,conn,data,isGroupMessage,sender):
        fileName =data['filename']
        f = open(self.homeFolder+'/'+fileName,'wb')
        while(True):
            msg=conn.recv(1024)
            if not msg:
                break
            if(isGroupMessage):
                 decrypted_data = crypto.decrypt_group_message(msg,self.grouplist[data['groupname']])
            else:
                decrypted_data=crypto.decrypt_p2p(msg,self.dhke.key1,self.dhke.key2,self.dhke.key3)
            f.write(decrypted_data)
        f.close()
        print(fileName ," received from ",sender)
      
    def sendFile(self,clientName,fileName):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        requestObj = {}
        requestObj['choice'] = 'get-client-port'
        requestObj['name']=clientName
        s.sendall(pickle.dumps(requestObj))
        client_port = pickle.loads(s.recv(1024))['port']
        f = open(self.homeFolder +"/"+fileName,'rb')
        messageObj = {}
        messageObj['sender']=self.name
        messageObj['type'] = 'file'
        messageObj['filename']=fileName
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.dhke1=diffie_hellman.DiffieHellman(self.rollnum)
        s.connect((HOST,client_port))
        self.dhke1.initiate_key_exchange(s)
        plain_text=json.dumps(messageObj).encode('utf-8')
        cipher_text=crypto.encrypt_p2p(plain_text,self.dhke1.key1,self.dhke1.key2,self.dhke1.key3)
        s.sendall(cipher_text)
        print(fileName ," sent")
        l = f.read(1023)
        while (l):
            cipher_text=crypto.encrypt_p2p(l,self.dhke1.key1,self.dhke1.key2,self.dhke1.key3)
            s.sendall(cipher_text)
            l = f.read(1023)
        f.close()
        s.close()

    def message(self,clientName,msg):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        requestObj = {}
        requestObj['choice'] = 'get-client-port'
        requestObj['name']=clientName
        s.sendall(pickle.dumps(requestObj))
        client_port = pickle.loads(s.recv(1024))['port']
        messageObj = {}
        messageObj['sender']=self.name
        messageObj['type'] = 'text'
        messageObj['msg']=msg
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.dhke1=diffie_hellman.DiffieHellman(self.rollnum)
        s.connect((HOST,client_port))
        self.dhke1.initiate_key_exchange(s)
        plain_text=json.dumps(messageObj).encode('utf-8')
        cipher_text=crypto.encrypt_p2p(plain_text,self.dhke1.key1,self.dhke1.key2,self.dhke1.key3)
        s.sendall(cipher_text)
        s.close()

    def join_group(self,name):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        requestObj = {}
        requestObj['name'] = self.name
        requestObj['choice'] = 'join-group'
        requestObj['groupname']=name
        requestObj['port'] =self.port
        s.sendall(pickle.dumps(requestObj))
        self.grouplist[name]=s.recv(1024).decode()
        s.close()

    def list_group(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        requestObj = {}
        requestObj['choice'] = 'list-group'
        s.sendall(pickle.dumps(requestObj))
        groupstring = s.recv(1024).decode()
        s.close()
        return groupstring

    def mess_group(self,groupName,message):
        if(groupName in self.grouplist.keys()):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((HOST,PORT))
            #print(self.grouplist[groupName])
            
            encryptedMessage = crypto.encrypt_group_msg(message.encode(),str(self.grouplist[groupName]))
            requestObj = {}
            requestObj['choice'] = 'message-group'
            requestObj['type'] = 'text'
            requestObj['name'] = self.name
            requestObj['initiator-port'] = self.port
            requestObj['groupname'] = groupName
            requestObj['msg'] = encryptedMessage
            s.sendall(pickle.dumps(requestObj))
            s.close()
        else:
            print("Not in group")

    def send_file_group(self,groupName,fileName):
        if(groupName in self.grouplist.keys()):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((HOST,PORT))
            requestObj = {}
            requestObj['choice'] = 'message-group'
            requestObj['groupname']=groupName
            requestObj['type'] = 'file'
            requestObj['initiator-port'] = self.port
            requestObj['filename']=fileName
            requestObj['name'] = self.name
            s.sendall(pickle.dumps(requestObj))
            f = open(self.homeFolder +"/"+fileName,'rb')
            l = f.read(1023)
            while (l):
                cipher_text= crypto.encrypt_group_msg(l,self.grouplist[groupName])
                s.sendall(cipher_text)
                l = f.read(1023)
            f.close()
            s.close()
        else:
            print("Not in group")


