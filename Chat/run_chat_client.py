from chatclient import ChatClient
from chatclient_gui import ChatClientGUI

def receive(client,window):
    message = client.receive_message()
    window.insert_on_gui_message_box(message):


if __name__ == '__main__':
  host = input("Host: ")
  port = input("Puerto: ")
  if not host:
    host = "localhost"

  if not port:
    port = 1234
  else:
    port = int(port)
