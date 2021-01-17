import socket,pickle
HOST = '127.0.0.1'
PORT = 54001

class client:
    def __init__(self,name,rollnum,pswd,port):
            self.name = name
            self.rollnum = rollnum
            self.pswd=pswd
            self.online = 0
            self.choice=-1
            self.port = port
    def signin(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        self.online = 1
        self.choice = 1
        s.send(pickle.dumps(self))
        print(s.recv(1).decode())
        s.close()
    def signup(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        self.choice = 2
        s.sendall(pickle.dumps(self))
        print(s.recv(1).decode())
        s.close()
    def server(self):
        host = '127.0.0.1'
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        print(self.port)
        server.bind((host,self.port))
        server.listen()
        while True:
            conn,addr=server.accept()
            print(conn.recv(1024).decode())
            print(addr)
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



