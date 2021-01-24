import clientlib
import socket,pickle
import json
import random
import crypto
import time

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
    def message(self,conn,data):
        if data['type'] =='file':
            chunk_array=[]
            while(True):
                    msg=conn.recv(1024)
                    if not msg:
                        break
                    chunk_array.append(msg)      
        for port in self.getportlist():
            if port==data['initiator-port']:
                continue
            client_sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client_sock.connect(('127.0.0.1',port))
            messageObj={}
            messageObj['groupname'] = self.grname
            if data['type'] =='text':
                messageObj['type'] = 'text' 
                messageObj['encrypted'] = data['msg']
                client_sock.sendall(pickle.dumps(messageObj))
            else:
                messageObj['type'] = 'file'
                messageObj['filename']=data['filename']
                client_sock.sendall(pickle.dumps(messageObj))
                for item in chunk_array:
                    time.sleep(1)
                    client_sock.sendall(item)
        if data['type']=='file':
            chunk_array.clear()
        client_sock.close()



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
                g.message(conn,data)
            conn.close()
                

