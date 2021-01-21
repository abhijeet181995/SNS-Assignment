import clientlib

print("**********Welcome to Chat Client*********")
port = int(input("Enter Port\n"))
s = clientlib.client(port,'client1')
while True:
    inpt = input("Enter Command\n>>").split()
    if inpt[0]=="signin" and s.online==0 :
        user = input("Enter Username\n")
        pswd = input("Enter Password\n")
        if s.signin(user,pswd):
            print("Sign In Success")
        else:
            print("Sign In Failed")
    elif inpt[0]=="signup" and s.online==0:
        user = input("Enter Username\n")
        rollnum = int(input("Enter Roll Number\n"))
        pswd = input("Enter Password\n")
        if s.signup(user,rollnum,pswd):
            print("Sign Up Success")
        else:
            print("Sign Up Failed")
    elif inpt[0]=="sendfile" and inpt[1]=="group" and s.online == 1:
        s.send_file_group(inpt[2],inpt[3])
    elif inpt[0]=="send" and inpt[1]=="group" and s.online == 1:
        s.mess_group(inpt[2],inpt[3])
    elif inpt[0]=="sendfile" and s.online==1:
        s.sendFile(inpt[1],inpt[2])
    elif inpt[0]=="send" and s.online==1:
        s.message(inpt[1],inpt[2])
    elif inpt[0]=="join":
        s.join_group(inpt[1])
    elif inpt[0]=="list":
        print(s.list_group())





