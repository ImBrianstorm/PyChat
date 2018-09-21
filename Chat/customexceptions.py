class ExistingUsernameException(Exception):
  pass

class PublicRoomException(Exception):
  pass

class ClientAlreadyInRoomException(Exception):
  pass

class NotInvitedClientException(Exception):
  pass

class ClientAlreadyInvitedException(Exception):
  pass

class NonexistentClientException(Exception):
  pass

class NonexistentChatRoomException(Exception):
  pass

class RoomAlreadyInServerException(Exception):
  pass

class InviterClientIsNotOwnerException(Exception):
  pass

class ClientNotFoundException(Exception):
  pass
