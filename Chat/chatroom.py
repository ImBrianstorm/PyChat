from customexceptions import (ExistingUsernameException, PublicRoomException,
                              ClientAlreadyInRoomException, NotInvitedClientException,
                              ClientAlreadyInvitedException, NonexistentClientException,
                              InviterClientIsNotOwnerException, ClientNotFoundException)

class ChatRoom:

  def __init__(self,room_owner=None,room_name="public_room",is_public=True):
    self.room_owner = room_owner
    self.room_name = room_name
    self.room_clients = []
    self.is_public = is_public
    if not self.is_public:
      self.room_clients.append(room_owner)
      self.invited_clients = [room_owner]

  def __str__(self):
    string = ""

    if self.is_public:
      string += "Public room"
    else:
      string += "Private room name: " + self.room_name

    if not self.is_public:
      string += "\nRoom owner: " + self.room_owner.get_username()

    if not self.room_clients:
      string += "\nThere's no clients in the room."
    else:
      string += "\nClients:"
      for client in self.room_clients:
        string += "\n\t- " + client.get_username()

    if not self.is_public:
      string += "\nInvited clients:"
      for client in self.invited_clients:
        string += "\n\t- " + client.get_username()

    return string

  def get_room_owner(self):
    return self.room_owner

  def get_room_name(self):
    return self.room_name

  def get_client_names(self):
    for client in self.room_clients:
      yield client.get_username()

  def get_client_by_username(self,username):
    for client in self.room_clients:
      if client.get_username() == username:
        return client
    raise ClientNotFoundException("No se encontro el cliente en la sala")

  def room_is_public(self):
    return self.is_public

  def set_room_owner(self,room_owner):
    self.room_owner = room_owner

  def set_room_name(self,room_name):
    self.room_name = room_name

  def invite_client(self,invited_client,inviter_client):
    if self.room_is_public():
      raise PublicRoomException("No puedes invitar a un cliente a una sala de chat publica")
    else:
      if inviter_client is not self.room_owner:
        raise InviterClientIsNotOwnerException("El invitador no puede invitar clientes si no es dueño de la sala")
      else:
        if invited_client in self.invited_clients:
          raise ClientAlreadyInvitedException("Este cliente ya ha sido invitado")
        else:
          self.invited_clients.append(invited_client)

  def client_found(self,client):
    for room_client in self.room_clients:
      if room_client is client:
        return True
    return False

  def add_client(self,client):
    if client in self.room_clients:
      raise ClientAlreadyInRoomException("El cliente ya existe en la sala de chat")
    else:
      if self.is_public:
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
      if client.get_username() == name:
        raise ExistingUsernameException("El nombre de usuario ya existe en esta sala de chat")

  def broadcast(self,message,client_exception=None):
    for client in self.room_clients:
      if client is not client_exception:
        client.get_server_socket().send(bytes(message,"utf-8"))
