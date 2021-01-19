import socket
import random
import hashlib

class DiffieHellman:
    prime=1124685973
    alpha=1124685956
    
    def __init__(self,roll_num):
        self.private_key1=int(str(roll_num)+str(random.randint(0,self.prime-1)))
        self.private_key2=int(str(roll_num)+str(random.randint(0,self.prime-1)))
        self.private_key3=int(str(roll_num)+str(random.randint(0,self.prime-1)))
        self.public_key1=pow(self.alpha,self.private_key1,self.prime)
        self.public_key2=pow(self.alpha,self.private_key2,self.prime)
        self.public_key3=pow(self.alpha,self.private_key3,self.prime)
        self.key1=int()
        self.key2=int()
        self.key3=int()
        pass
    
    #currently returning 64-bit key in bytes(data type of python)
    def key_calculator(self,private_key,public_key):
        session_key=pow(public_key,private_key,self.prime)
        session_key=hashlib.sha256(str(session_key)).digest()[0:8]
        return session_key

    def initiate_key_exchange(self,s):
        s.sendall(b'DHKE')
        if s.recv(1024)!=b'OK':
            return
        #sending and recieving public key1 and calculating key1
        s.sendall(str(self.public_key1).encode('utf-8'))
        recv=bytearray()
        while True:
            temp_recv=s.recv(1024)
            recv+=temp_recv
            if(len(temp_recv))<1024:
                break
        other_public_key1=int(recv.decode('utf-8'))
        self.key1=self.key_calculator(self.private_key1,other_public_key1)

        #sending and recieving public key1 and calculating key2
        s.sendall(str(self.public_key2).encode('utf-8'))
        recv=bytearray()
        while True:
            temp_recv=s.recv(1024)
            recv+=temp_recv
            if(len(temp_recv))<1024:
                break
        other_public_key2=int(recv.decode('utf-8'))
        self.key2=self.key_calculator(self.private_key2,other_public_key2)

        #sending and recieving public key1 and calculating key3
        s.sendall(str(self.public_key3).encode('utf-8'))
        recv=bytearray()
        while True:
            temp_recv=s.recv(1024)
            recv+=temp_recv
            if(len(temp_recv))<1024:
                break
        other_public_key3=int(recv.decode('utf-8'))
        self.key3=self.key_calculator(self.private_key3,other_public_key3)
        print("Other public key1 ",other_public_key1)
        print("Other public key2 ",other_public_key2)
        print("Other public key3 ",other_public_key3)
        pass

    def party2_key_exchange(self,sock):
        sock.sendall(b'OK')

        #recieve and send public key 1
        recv=bytearray()
        while True:
            temp_recv=sock.recv(1024)
            recv+=temp_recv
            if(len(temp_recv))<1024:
                break
        other_public_key1=int(recv.decode('utf-8'))
        self.key1=self.key_calculator(self.private_key1,other_public_key1)
        sock.sendall(str(self.public_key1).encode('utf-8'))


        #recieve and send public key 2
        recv=bytearray()
        while True:
            temp_recv=sock.recv(1024)
            recv+=temp_recv
            if(len(temp_recv))<1024:
                break
        other_public_key2=int(recv.decode('utf-8'))
        self.key2=self.key_calculator(self.private_key2,other_public_key2)
        sock.sendall(str(self.public_key2).encode('utf-8'))

        #recieve and send public key 2
        recv=bytearray()
        while True:
            temp_recv=sock.recv(1024)
            recv+=temp_recv
            if(len(temp_recv))<1024:
                break
        other_public_key3=int(recv.decode('utf-8'))
        self.key3=self.key_calculator(self.private_key3,other_public_key3)
        sock.sendall(str(self.public_key3).encode('utf-8'))
        print("Other public key1 ",other_public_key1)
        print("Other public key2 ",other_public_key2)
        print("Other public key3 ",other_public_key3)
        pass