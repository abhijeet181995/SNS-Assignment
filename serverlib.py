import clientlib
import socket,pickle

HOST = '127.0.0.1'
PORT = 54005

class group:
    def __init__(self,name):
        self.grname = name
        self.membercount=0
        self.memberdic = {}
    def addmember(self,name,port):
        self.memberdic[name]=port
        self.membercount=self.membercount+1
    def getportlist(self):
        return [self.memberdic[name] for name in self.memberdic.keys()]


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
            if data['choice']=='signin':
                if data['name'] in self.clientlist.keys() and self.clientlist[data['name']]['pswd']==data['pswd']:
                    self.clientlist[data['name']]['online']=1
                    conn.send(b"1")
                else:
                    conn.send(b"0")
            if data['choice']=='signup':
                self.clientlist[data['name']]=data
                print(data['name'])
                conn.send(b"1")
            if data['choice']=='get-client-port':
                print(data['name'])
                print(self.clientlist[data['name']])
                data['port'] = self.clientlist[data['name']]['port']
                conn.sendall(pickle.dumps(data))
            if data['choice']=='join-group':
                if data['groupname'] in self.grouplist.keys():
                    self.grouplist[data['groupname']].addmember(data['name'],data['port'])
                else:
                    g = group(data['groupname'])
                    g.addmember(data['name'],data['port'])
                    self.grouplist[data['groupname']]=g
            if data['choice']=='list-group':
                groupstring = [[self.grouplist[name].grname,self.grouplist[name].membercount] for name in self.grouplist.keys()]
                conn.sendall(str(groupstring).encode())


            
            if data['choice']=='message-group':
                for port in g.getportlist():
                    m= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    m.connect(('127.0.0.1',port))
                    messageObj={}
                    messageObj['type'] = 'text'
                    messageObj['msg']=data.msg
                    m.send(pickle.dumps(messageObj))
                    m.close()
                

