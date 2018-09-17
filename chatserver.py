from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class ChatServer:

  def __init__(self, host="", port=1234):
    self.host = host
    self.port = port
    self.bufsize = 1024
    self.server_socket = None
    self.connected = False
    self.clients = []
    self.addresses = {}

  def __str__(self):
    string = "Server "
    if self.is_connected():
      return string + "conectado en el puerto " + str(self.port)
    else:
      return string + "desconectado"

  def start_server(self):
    self.server_socket = socket(AF_INET, SOCK_STREAM)
    address = (self.host,self.port)
    self.server_socket.bind(address)
    self.server_socket.listen()
    self.connected = True

  def shutdown_server(self):
    if self.server_socket != None:
      self.server_socket.close()
      self.server_socket = None
      self.connected = False

  def is_connected(self):
    return self.connected

  def get_host(self):
    return self.host

  def get_port(self):
    return self.port

  def get_bufsize(self):
    return self.bufsize

  def get_socket(self):
    return self.server_socket

  def set_host(self, host):
    self.host = host

  def set_port(self, port):
    self.port = port

  def set_bufsize(self, bufsize):
    self.bufsize = bufsize

  def set_socket(self, server_socket):
    if server_socket == None:
      self.shutdown_server()
    else:
      self.server_socket = server_socket
