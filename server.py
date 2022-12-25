import socket
import threading 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host=input("Enter your LAN IP: ")
port = 9999
print(host,port)
server.bind((host, port))
server.listen(10)
clients = []
usernames = []
dictionary={}
def broadcast(message):
    for client in clients:
        client.send(message)
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode('ascii'))
            del dictionary[username]
            usernames.remove(username)
            break
def sendall(message):
    for client in clients:
        client.send(message)
def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)
        print("Username is {}".format(username))
        dictionary[username]=address[1]
        sendall("{} joined!".format(username).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()
