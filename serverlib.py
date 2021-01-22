import clientlib
import socket,pickle
import json
import random
import crypto

HOST = '127.0.0.1'
PORT = 54005

class group: 
    def __init__(self,name):
        self.grname = name
        self.membercount=0
        self.memberdic = {}
        self.nounce=str(random.randint(0,655365))
    def addmember(self,name,port):
        self.memberdic[name]=port
        self.membercount=self.membercount+1
        return self.nounce
    def getportlist(self):
        return [self.memberdic[name] for name in self.memberdic.keys()]
    def message(self,msg):
        for port in self.getportlist():
            m= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            m.connect(('127.0.0.1',port))
            encrypted = crypto.encrypt_group_msg(msg.encode(),self.nounce)
            # messageObj['groupname'] = data['groupname']
            # messageObj['type'] = 'text' #group encrption object
            # messageObj['msg']=data['msg'] #intiate group key exchange
            m.sendall(self.grname.encode()+b" "+encrypted)
            m.close()



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
                    conn.sendall(self.grouplist[data['groupname']].nounce.encode())
                else:
                    g = group(data['groupname'])
                    g.addmember(data['name'],data['port'])
                    self.grouplist[data['groupname']]=g
                    conn.sendall(g.nounce.encode())
                print([name for name in self.grouplist.keys()])
            if data['choice']=='list-group':
                print([name for name in self.grouplist.keys()])
                groupstring = [[self.grouplist[name].grname,self.grouplist[name].membercount] for name in self.grouplist.keys()]
                conn.sendall(str(groupstring).encode())
            if data['choice']=='message-group':
                g = self.grouplist[data['groupname']]
                g.message(data['msg'])
                

