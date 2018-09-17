from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class ChatClient:

  def __init__(self, name, host, port):
    self.name = name
    self.host = host
    self.port = port
    self.address = (host,port)
    self.client_socket = None
    self.connected = False

  def __str__(self):
    string = self.name + " -> " + self.host + ":" + str(self.port)
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

  def is_connected(self):
    return self.connected

  def get_name(self):
    return self.name

  def get_host(self):
    return self.host

  def get_port(self):
    return self.port

  def get_address(self):
    return self.address

  def get_socket(self):
    return self.client_socket

  def set_name(self, name):
    self.name = name

  def set_host(self, host):
    self.host = host

  def set_port(self, port):
    self.port = port

  def set_address(self, address):
    self.address = address

  def set_socket(self, client_socket):
    if client_socket == None:
      self.close_socket()
    else:
      self.client_socket = client_socket
