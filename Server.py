import pickle
import socket
import threading
import rsa

hostIP = socket.gethostname()    # My local IP adress
port = 5555

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((hostIP,port))

server.listen()

clients=[]
nicknames=[]

(public_key,private_key) = pickle.load(open("shared.pkl", "rb")) # Gets the encryption keys

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message= client.recv(1024)
            broadcast(message) # Sends the recieved message to all the other clients
        except:
            index= clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f"{nickname} has Disconnected from the server \n")
            nicknames.remove(nickname)


def main():
    while True:
        client, address= server.accept()

        client.send("NICK".encode('utf-8'))
        nickname=client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        broadcast((f"{nickname} has connected to the server \n").encode('utf-8'))
        client.send("Connected to the server \n".encode('utf-8'))

        thread= threading.Thread(target=handle, args=(client,))
        thread.start()


print("server is running...")
main()