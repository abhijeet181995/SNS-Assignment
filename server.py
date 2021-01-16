import clientlib
import socket,pickle

HOST = '127.0.0.1'
PORT = 54001

clientlist = {}
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
server.bind((HOST,PORT))
server.listen()

while True:
    conn,addr=server.accept()
    data = pickle.loads(conn.recv(2048))
    if data.choice==1:
        if data.name in clientlist.keys():
            clientlist[data.name].online=1
            conn.send(b"1")
        else:
            conn.send(b"0")
        
    if data.choice==2:
        clientlist[data.name]=data
        print(data.name)
        conn.send(b"1")
    if data.choice==3:
        data.port = clientlist[data.name].port
        conn.sendall(pickle.dumps(data))

    conn.close()

server.close()