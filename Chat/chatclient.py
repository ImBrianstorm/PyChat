from socket import socket, AF_INET, SOCK_STREAM

class ChatClient:

  def __init__(self, username, host="localhost", port=1234,status="ACTIVE"):
    self.username = username
    self.host = host
    self.port = port
    self.status = status
    self.address = (host,port)
    self.client_socket = None
    self.server_socket = None
    self.connected = False

  def __str__(self):
    string = self.username + " -> " + self.host + ":" + str(self.port)
    if self.is_connected():
        string += " [CONNECTED]"
    else:
        string += " [DISCONNECTED]"
    return string

  def init_socket(self):
    self.client_socket = socket(AF_INET, SOCK_STREAM)
    self.client_socket.connect(self.address)
    self.connected = True

  def close_socket(self):
    if self.client_socket != None:
      self.client_socket.close()
      self.client_socket = None
      self.connected = False

  def close_server_socket(self):
    if self.server_socket != None:
      self.server_socket.close()
      self.server_socket = None

  def is_connected(self):
    return self.connected

  def receive_message(self):
      message = client_socket.recv(BUFSIZ).decode("utf-8")
      return message

  def send(self,message):
    self.client_socket.send(bytes(msg, "utf-8"))
    if msg == "DISCONNECT":
        self.client_socket.close()

  def get_username(self):
    return self.username

  def get_host(self):
    return self.host

  def get_port(self):
    return self.port

  def get_address(self):
    return self.address

  def get_socket(self):
    return self.client_socket

  def get_server_socket(self):
   return self.server_socket

  def get_status(self):
    return self.status

  def set_username(self, username):
    self.username = username

  def set_host(self, host):
    self.host = host

  def set_port(self, port):
    self.port = port

  def set_address(self, address):
    self.address = address

  def set_socket(self, client_socket):
    self.close_socket()
    if client_socket is not None:
      self.connected = True
      self.client_socket = client_socket

  def set_server_socket(self,server_socket):
    self.close_server_socket()
    if server_socket is not None:
      self.connected = True
      self.server_socket = server_socket

  def set_status(self,status):
    self.status = status
