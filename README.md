# RSA-encrypted-chat-room
![enter image description here](https://img.shields.io/badge/Version-Alpha-green)

This is a public chat room where you can talk to other people safely.
This project was for me to exercise some basic networking and encryption principles.


## How to use?
Run the Server.py file on the server machine. To allow external connections, you need to allow port forwarding on port 5555 in your router, and allow the same port thourgh your firewall.
Each client who wish to connect to the server, has to run the Client.py file and set a username.

## How it works?
* The server send the client a request for a nick name and public key.
* The client send back the nickname and his unique public key.
* The server then send the symetric session encryption key after it has been encrypted by the client's public key.
* The client recieves the message and decrypt it using his private key.
* From this point, both the client and the server share the same session key, which they use to communicate.
