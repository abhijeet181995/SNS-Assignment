import clientlib

print("**********Welcome to Chat Client*********")

while True:
    user = input("Enter Username")
    rollnum = input("Enter Roll Number") 
    pswd = input("Enter Password")
    port = input("Enter Port")
    s = clientlib.client(user,rollnum,pswd,port)
    s.signup()
    s.signin()
    s.message("B","Yes")




