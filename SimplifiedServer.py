import socket
import pickle
import rsa
from Crypto.Cipher import AES


(public_key,private_key) = pickle.load(open("shared.pkl", "rb")) # Gets the encryption keys


hostIP = socket.gethostname()    # My local IP adress
port = 5555
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((hostIP,port))

server.listen()

key = "This is the key!".encode('utf-8')
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest("Hello world".encode('utf-8'))
print(ciphertext)
cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

plaintext = cipher.decrypt(ciphertext)
print(plaintext)

while True:
    client, address= server.accept()

    client.send("NICK".encode('utf-8'))
    msg=client.recv(1024)
    decmsg=rsa.decrypt(msg,private_key)
    print(decmsg.decode('utf-8'))

