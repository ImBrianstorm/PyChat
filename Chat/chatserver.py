from customexceptions import (ExistingUsernameException, NonexistentChatRoomException,
                             RoomAlreadyInServerException, ClientNotFoundException,
                             InviterClientIsNotOwnerException, ClientAlreadyInvitedException,
                             ClientAlreadyInRoomException, NotInvitedClientException)
from chatclient import ChatClient
from chatroom import ChatRoom
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from threading import Thread

class ChatServer:

  def __init__(self, host="0.0.0.0", port=1234):
    self.host = host
    self.port = port
    self.bufsize = 1024
    self.server_socket = None
    self.connected = False
    self.public_room = ChatRoom()
    self.chatroom_list = [self.public_room]

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
    print("Server conectado en el puerto " + str(self.port) + "...")
    print("Presione ctrl+c para apagar...")
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
    welcome = "¡Bienvenido a PyChat!"
    client_socket.send(bytes(welcome, "utf-8"))

    identified, client = self.identify_client(client_socket,client_address)

    if identified:
      while client.is_connected():
        message = client.get_server_socket().recv(self.bufsize).decode("utf-8").strip()
        if message != "DISCONNECT":
          self.process_message(message,client)
        else:
          name = client.get_username()
          host,port = client_address
          client_socket.close()
          self.remove_from_all_chatrooms(client)
          leave_message = "%s se ha ido :(" % name
          print("{} ({}:{}) se ha desconectado...".format(name,host,port))
          self.public_room.broadcast(leave_message)
          break

  def identify_client(self,client_socket,client_address):
    not_identified = True

    while not_identified:
      sleep(0.3)
      identify = "Ingresa 'IDENTIFY username' (donde username es el nombre que usarás)"
      client_socket.send(bytes(identify, "utf-8"))
      sleep(0.3)
      disconnect = "O bien, ingresa 'DISCONNECT' para salir"
      client_socket.send(bytes(disconnect, "utf-8"))
      message = client_socket.recv(self.bufsize).decode("utf-8")

      if message.startswith("IDENTIFY"):
        name = message[len("IDENTIFY "):]
        try:
          self.public_room.verify_name(name)
        except ExistingUsernameException:
          username_error = '"%s" ya está en uso. Prueba con otro\n' % name
          client_socket.send(bytes(username_error, "utf-8"))
          continue
        host,port = client_address
        client = ChatClient(name,host,port)
        client.set_server_socket(client_socket)
        print('{}:{} se ha identificado como: {}'.format(host,port,name))
        greeting = '¡Hola %s! Ahora puedes comenzar a disfrutar de PyChat :)' % name
        client_socket.send(bytes(greeting, "utf-8"))
        join_message = "%s se ha unido al chat. ¡Sé amable y di hola!" % name
        self.public_room.broadcast(join_message)
        self.public_room.add_client(client)
        return True, client

      elif message == "DISCONNECT":
        goodbye = 'Hasta luego :)'
        client_socket.send(bytes(goodbye, "utf-8"))
        sleep(0.3)
        client_socket.close()
        print("Un cliente no identificado con la direccion %s:%s se ha ido" % client_address)
        return False, None

      error = "¡Creo que has cometido un error!"
      client_socket.send(bytes(error, "utf-8"))

  def process_message(self,message,client):
    # STATUS userstatus
    if message.startswith("STATUS "):
      userstatus = message[len("STATUS "):]
      if userstatus == "ACTIVE" or userstatus == "AWAY" or userstatus == "BUSY":
        client.set_status(userstatus)
        success_message = 'Se te ha asignado el estado "' + userstatus + '"'
        client.get_server_socket().send(bytes(success_message,"utf-8"))
      else:
        error = 'No puedes asignar un status distinto a "ACTIVE", "AWAY" o "BUSY"'
        client.get_server_socket().send(bytes(error,"utf-8"))

    # USERS
    elif message == "USERS":
      users = "Usuarios: "
      usernames = []
      for room_client in self.public_room.room_clients:
        username = room_client.get_username()
        status = room_client.get_status()
        usernames.append(username + "(" + status + ")")
      users += ", ".join(usernames)
      client.get_server_socket().send(bytes(users,"utf-8"))

    # MESSAGE username messageContent
    elif message.startswith("MESSAGE "):
      message_args = message.split(" ")[1:]
      if len(message_args)!=2:
        error = "No escribiste el numero correcto de argumentos (username, messageContent)"
        client.get_server_socket().send(bytes(error,"utf-8"))
      else:
        try:
          username = self.public_room.get_client_by_username(message_args[0])
          if username is client:
             message = "¡Vamos, " + client.get_username() + "! ¿Por qué no hablar con alguien más? :)"
             client.get_server_socket().send(bytes(message,"utf-8"))
          else:
            message_from = "Mensaje privado de " + client.get_username() + ": " + message_args[1]
            message_to = "Mensaje privado para " + username.get_username() + ": " + message_args[1]
            username.get_server_socket().send(bytes(message_from,"utf-8"))
            client.get_server_socket().send(bytes(message_to,"utf-8"))
        except ClientNotFoundException:
          error = "El usuario al que intentas mandar un mensaje no existe :("
          client.get_server_socket().send(bytes(error,"utf-8"))

    # PUBLICMESSAGE messageContent
    elif message.startswith("PUBLICMESSAGE "):
      message = client.get_username() + ": " + message[len("PUBLICMESSAGE "):]
      self.public_room.broadcast(message)

    # CREATEROOM roomname
    elif message.startswith("CREATEROOM "):
      roomname = message[len("CREATEROOM "):]
      if not roomname:
        error = "No especificaste un nombre para la sala de chat"
        client.get_server_socket().send(bytes(error,"utf-8"))
      elif " " in roomname:
        error = "No puedes usar espacios al crear una sala de chat :/"
        client.get_server_socket().send(bytes(error,"utf-8"))
      else:
        try:
          new_chatroom = ChatRoom(room_owner=client,room_name=roomname,is_public=False)
          self.add_chat_room(new_chatroom)
          message = "¡Has creado la sala de chat " + roomname + "! Ya puedes invitar a tus amigos :)"
          client.get_server_socket().send(bytes(message,"utf-8"))
        except RoomAlreadyInServerException:
          error = "Ya existe una sala llamada " + roomname + ", intenta con otro nombre :D"
          client.get_server_socket().send(bytes(error,"utf-8"))

    # INVITE roomname username1, username2...
    elif message.startswith("INVITE "):
      invite_args = message.split(" ")[1:]
      if len(invite_args) < 2:
        error = "No escribiste el número correcto de argumentos (roomname username1 username2 ...)"
        client.get_server_socket().send(bytes(error,"utf-8"))
      else:
        try:
          invitation = client.get_username() + ' te ha invitado a su sala de chat "' + invite_args[0] + '"'
          for client_name in invite_args[1:]:
            invited_client = self.public_room.get_client_by_username(client_name)
            self.get_chat_room(invite_args[0]).invite_client(invited_client,client)
            invited_client.get_server_socket().send(bytes(invitation,"utf-8"))
          success_message = "Invitaste a " + ", ".join(invite_args[1:]) + ' a ' + invite_args[0]
          client.get_server_socket().send(bytes(success_message,"utf-8"))
        except ClientNotFoundException:
          error = "Al menos uno de los usuarios especificados no existe :/"
          client.get_server_socket().send(bytes(error,"utf-8"))
        except InviterClientIsNotOwnerException:
          error = "No eres propietario de esta sala :("
          client.get_server_socket().send(bytes(error,"utf-8"))
        except ClientAlreadyInvitedException:
          error = "Ya has invitado al menos a alguno de estos usuarios"
          client.get_server_socket().send(bytes(error,"utf-8"))
        except NonexistentChatRoomException:
          error = 'No existe la sala '+ invite_args[0]
          error += ', pero puedes crearla con "CREATEROOM ' + invite_args[0] + '" :)'
          client.get_server_socket().send(bytes(error,"utf-8"))

    # JOINROOM room_name
    elif message.startswith("JOINROOM "):
      room_name = message[len("JOINROOM "):]
      try:
        self.get_chat_room(room_name).add_client(client)
        success_message = 'Te has unido a la sala de chat "' + room_name + '", ¡di hola! :)'
        client.get_server_socket().send(bytes(success_message,"utf-8"))
        join_message = client.get_username() + ' se ha unido a "' + room_name + '",¡dile hola! :D'
        self.get_chat_room(room_name).broadcast(join_message,client_exception=client)
      except NonexistentChatRoomException:
        error = 'No existe la sala de chat a la que quieres unirte, pero puedes crearla con '
        error += '"CREATEROOM ' + room_name + '" ;)'
        client.get_server_socket().send(bytes(error,"utf-8"))
      except ClientAlreadyInRoomException:
        error = "Ya estás en esta sala de chat :O"
        client.get_server_socket().send(bytes(error,"utf-8"))
      except NotInvitedClientException:
        error = "¡Demonios! No has sido invitado a " + room_name + " :("
        client.get_server_socket().send(bytes(error,"utf-8"))

    # ROOMESSAGE roomname messageContent
    elif message.startswith("ROOMESSAGE "):
      room_message_args = message.split(" ")[1:]
      if len(room_message_args) != 2:
        error = "No escribiste el número correcto de argumentos (roomname messageContent)"
        client.get_server_socket().send(bytes(error,"utf-8"))
      else:
        try:
          if self.get_chat_room(room_message_args[0]).client_found(client):
            message = client.get_username() + " en "  + room_message_args[0] + ": " + room_message_args[1]
            self.get_chat_room(room_message_args[0]).broadcast(message)
          else:
            error = "No puedes mandar mensajes a esta sala de chat porque no estás en ella :("
            client.get_server_socket().send(bytes(error,"utf-8"))
        except NonexistentChatRoomException:
          error = "No puedes mandar mensajes a esta sala de chat porque no existe, "
          error = 'pero puedes crearla con "CREATEROOM ' + room_message_args[1] + '"'
          client.get_server_socket().send(bytes(error,"utf-8"))

    #DEFAULT
    else:
      error = "El mensaje enviado no es valido"
      client.get_server_socket().send(bytes(error,"utf-8"))

  def is_connected(self):
    return self.connected

  def add_chat_room(self,chatroom):
    if self.chatroom_name_exists(chatroom.get_room_name()):
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
      if room.client_found(client):
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
        self.connected = True
        self.server_socket.close()
      self.server_socket = server_socket
