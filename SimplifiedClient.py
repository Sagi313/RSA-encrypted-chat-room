import socket
import pickle
import rsa

(public_key,private_key) = pickle.load(open("shared.pkl", "rb")) # Gets the encryption keys


hostIP = socket.gethostname()    # My local IP adress
port = 5555
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((hostIP,port))
msg="test".encode('utf-8')
encmsg=rsa.encrypt(msg,public_key)

sock.send(encmsg)
