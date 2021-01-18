import socket,pickle
import threading
HOST = '127.0.0.1'
PORT = 54005

class client:
    def __init__(self,port):
            self.port = port
            self.online = 0
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
        host = '127.0.0.1'
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        server.bind((host,self.port))
        server.listen()
        while True:
            conn,addr=server.accept()
            print(conn.recv(1024).decode())
            print(addr)
            conn.close()
    def message(self,name,msg):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        cpy = self
        cpy.choice = 3
        cpy.name = name
        s.sendall(pickle.dumps(cpy))
        port = pickle.loads(s.recv(1024)).port
        s.close()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,port))
        s.send(msg.encode())
        s.close()



