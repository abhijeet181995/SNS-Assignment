import clientlib
import socket,pickle

HOST = '127.0.0.1'
PORT = 54005

class server:
    def __init__(self):
        self.s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        self.s.bind((HOST,PORT))
        self.clientlist={}
        self.grouplist={}
        self.s.listen()
        while True:
            conn,addr=self.s.accept()
            data = pickle.loads(conn.recv(1024))
            if data.choice==1:
                if data.name in self.clientlist.keys() and self.clientlist[data.name].pswd==data.pswd:
                    self.clientlist[data.name].online=1
                    conn.send(b"1")
                else:
                    conn.send(b"0")
            if data.choice==2:
                self.clientlist[data.name]=data
                print(data.name)
                conn.send(b"1")
            if data.choice==3:
                data.port = self.clientlist[data.name].port
                conn.sendall(pickle.dumps(data))
                

