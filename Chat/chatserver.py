from customexceptions import (ExistingUsernameException, PublicRoomException,
                              ClientAlreadyInRoomException, NotInvitedClientException,
                              ClientAlreadyInvitedException, NonexistentClientException,
                              NonexistentChatRoomException, RoomAlreadyInServerException)
from chatclient import ChatClient
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class ChatServer:

  def __init__(self, host="", port=1234):
    self.host = host
    self.port = port
    self.bufsize = 1024
    self.server_socket = None
    self.connected = False
    self.clients_list = []
    self.chatroom_list = [ChatRoom()]

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
    print("Esperando por conexiones...")

  def shutdown_server(self):
    if self.server_socket != None:
      self.server_socket.close()
      self.server_socket = None
      self.connected = False

  def accept_client(self):
    client_socket, client_address = self.server_socket.accept()
    print("%s:%s se ha conectado..." % client_address)
    Thread(target=self.handle_client, args=(client_socket, client_address)).start()

  def handle_client(self,client_socket,client_address):
    identified, client = self.identify_client(client_socket,client_address)
    if identified:
      while client.is_connected():
        message = client.get_socket().recv(self.bufsize).decode("utf-8").strip()
        if message != "DISCONNECT":
          self.process_message(message)
        else:
          name = client.get_name()
          client.close_socket()
          self.remove_from_all_chatrooms(client)
          leave_message = "%s se ha ido :(" % name
          print("%s se ha desconectado" % name)
          get_chat_room("public_room").broadcast(leave_message)
          break

  def identify_client(self,client_socket,client_address):
    not_identified = True
    welcome = '¡Bienvenido a Pychat!\n'
    client_socket.send(bytes(welcome, "utf-8"))

    while not_identified:
      identify = 'Ingresa "IDENTIFY username" (donde username es el nombre que usarás)\n'
      disconnect = 'O bien, ingresa "DISCONNECT" para salir'
      client_socket.send(bytes(identify, "utf-8"))
      client_socket.send(bytes(disconnect, "utf-8"))
      message = client_socket.recv(self.bufsize).decode("utf-8").strip()

      if message.startswith("IDENTIFY"):
        name = message[len("IDENTIFY "):]
        try:
          self.get_chat_room("public_room").verify_name(name)
        except ExistingUsernameException:
          username_error = '%s ya existe en el server. Intentalo de nuevo' % name
          client_socket.send(bytes(username_error, "utf-8"))
          continue
        host,port = client_address
        client = ChatClient(name,host,port)
        client.set_address(client_address)
        client.set_server_socket(client_socket)
        print('{}:{} se ha identificado como: {}'.format(host,port,name))
        greeting = '¡Hola %s! Ahora puedes comenzar a mandar mensajes' % name
        client_socket.send(bytes(greeting, "utf-8"))
        join_message = "%s se ha unido al chat. ¡Sé amable y di hola!" % name
        self.get_chat_room("public_room").broadcast(join_message)
        self.clients_list.append(client)
        return True, client

      elif message == "DISCONNECT":
        goodbye = 'Hasta luego, pasajero :)'
        client_socket.send(bytes(goodbye, "utf-8"))
        client_socket.close()
        print("Un cliente no identificado con la direccion %s:%s se ha ido" % client_address)
        return False, None

      error = "¡Creo que has cometido un error!"
      client_socket.send(bytes(error, "utf-8"))

  def process_message(self,message):
    message = message.strip()
    # STATUS userstatus
    # USERS
    # MESSAGE username messageContent
    # PUBLICMESSAGE messageContent
    # CREATEROOM roomname
    # INVITE roomname username1, username,2
    # JOINROOM room_name
    # ROOMESSAGE roomname messageContent
    # DISCONNECT

  def is_connected(self):
    return self.connected

  def add_chat_room(self,chatroom):
    if chatroom_name_exists(chatroom.get_room_name()):
      raise RoomAlreadyInServerException("Esta sala de chat ya existe en el server")
    else:
      self.chatroom_list.append(chatroom)

  def chatroom_name_exists(self,name):
    for room in self.chatroom_list:
      if room.get_room_name() == name:
        return True
    return False

  def get_chat_room(self,name):
    for room in self.chatroom_list:
      if room.get_room_name() == name:
        return room
    raise NonexistentChatRoomException("No existe la sala de chat a la que se desea acceder")

  def remove_from_all_chatrooms(self,client):
    for room in self.chatroom_list:
      if client in room:
        room.remove_client(client)

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
      if self.server_socket != None:
        self.server_socket.close()
      self.server_socket = server_socket

class ChatRoom:

  def __init__(self,room_owner=None,room_name="public_room",is_public=True):
    self.room_owner = room_owner
    self.room_name = room_name
    self.room_clients = []
    self.is_public = is_public
    if not self.is_public:
      self.room_clients.append(owner)
      self.invited_clients = []

  def get_room_owner(self):
    return self.room_owner

  def get_room_name(self):
    return self.room_name

  def room_is_public(self):
    return self.is_public

  def set_room_owner(self,room_owner):
    self.room_owner = room_owner

  def set_room_name(self,room_name):
    self.room_name = room_name

  def invite_client(self,client):
    if self.room_is_public():
      raise PublicRoomException("No puedes invitar a un cliente a una sala de chat publica")
    else:
      if client in self.invited_clients:
        raise ClientAlreadyInvitedException("Este cliente ya ha sido invitado")
      else:
          self.room_clients.append(client)

  def add_client(self,client):
    if client in self.room_clients:
      raise ClientAlreadyInRoomException("El cliente ya existe en la sala de chat")
    else:
      if self.is_public():
        self.room_clients.append(client)
      else:
        if client not in self.invited_clients:
          raise NotInvitedClientException("El cliente no ha sido invitado a la sala de chat")
        else:
          self.room_clients.append(client)
          self.invited_clients.remove(client)

  def remove_client(self,client):
    if client not in self.room_clients:
      raise NonexistentClientException("El cliente no esta en esta sala de chat")
    else:
      self.room_clients.remove(client)

  def verify_name(self,name):
    for client in self.room_clients:
      if client.getName() == name:
        raise ExistingUsernameException("El nombre de usuario ya existe en el server")

  def broadcast(self,message):
    for client in self.room_clients:
      client.get_server_socket().send(bytes(message,"utf-8"))
