import pickle
import socket
import threading
import tkinter.scrolledtext
from tkinter import simpledialog
import tkinter as tk
import rsa


the_hostIP = socket.gethostname()    # My local IP adress
the_port = 5555

(public_key,private_key) = pickle.load(open("shared.pkl", "rb")) # Gets the encryption keys


class Client:
    def __init__(self,hostIP,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((hostIP,port))

        nickname_popup=tk.Tk()
        nickname_popup.withdraw()

        self.nickname= simpledialog.askstring("Nickname", "please choose a nickaname", parent=nickname_popup)  # First popup Window

        self.gui_done = False
        self.running = True

        gui_thread= threading.Thread(target=self.gui_loop)
        receive_thread= threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.window=tk.Tk()
        self.window.title("RSA Encrypted Chat")
        self.window.configure()

        self.chat_label= tk.Label(self.window,text="chat")
        self.chat_label.pack(padx=20,pady=5)

        self.text_area=tkinter.scrolledtext.ScrolledText(self.window)
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state='disabled') # So the user won't be able to change the chat history


        
        self.input_area=tk.Text(self.window,height=3)
        self.input_area.pack(padx=20,pady=5)

        self.send_button= tk.Button(self.window, text="send",command=self.send)
        self.send_button.pack()


        self.gui_done=True
        self.window.mainloop()

    def send(self):
        message = f"{self.nickname}: {self.input_area.get('1.0','end')}"

        #encrypt_message=rsa.encrypt(message.encode('utf-8'),public_key) ####
        #decrypt_message=rsa.decrypt(encrypt_message,private_key)        

        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0','end') # Cleaning the input text box when sending
    

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                #message = self.sock.recv(1024)
                #message=rsa.decrypt(message, private_key).decode('utf-8')
                #decrypt_message=rsa.decrypt(message,private_key)
                
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

    def stop(self):
        self.running=False
        self.window.destroy()
        self.sock.close()
        exit(0)


client= Client(the_hostIP,the_port)  