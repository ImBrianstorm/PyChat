from chatclient import ChatClient
from chatclient_gui import ChatClientGUI
from threading import Thread
from tkinter import Tk

def receive(client,window):
    while True:
      try:
        message = client.receive_message()
        window.insert_on_gui_message_box(message)
      except OSError:
        break

def close_function(client):
    client.send("DISCONNECT")

if __name__ == '__main__':
  host = input("Host: ")
  port = input("Puerto: ")
  if not host:
    host = "localhost"

  if not port:
    port = 1234
  else:
    port = int(port)

  client = ChatClient(None,host,port,"ACTIVE")
  client.init_socket()
  root = Tk()
  root.geometry("500x400")
  app = ChatClientGUI(root,close_function,client.send,client)

  Thread(target=receive,args=(client,app)).start()
  root.mainloop()
