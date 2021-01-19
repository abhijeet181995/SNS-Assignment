import socket,pickle
import threading
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
            data = pickle.loads(conn.recv(1024))
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
            f.write(data)
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
        messageObj = {}
        messageObj['type'] = 'file'
        messageObj['fileName'] = fileName
        s.send(pickle.dumps(messageObj))
        print(fileName ," sent")
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
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
        s.connect((HOST,port))
        s.send(pickle.dumps(messageObj))
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


