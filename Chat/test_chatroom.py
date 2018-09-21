from chatroom import ChatRoom
from chatclient import ChatClient
from socket import socket, AF_INET, SOCK_STREAM
import customexceptions
import unittest

class TestChatRoom(unittest.TestCase):

    def setUp(self):
        self.client = ChatClient("Mauricio")
        self.client2 = ChatClient("Aglae")
        self.public_room = ChatRoom()
        self.private_room = ChatRoom(self.client,"foo",False)

    def test_str_public(self):
        self.assertEqual(self.public_room.__str__(),"Public room\nThere's no clients in the room.")

    def test_str_private(self):
        self.assertEqual(self.private_room.__str__(),"Private room name: foo\n"
                                                   + "Room owner: Mauricio\n"
                                                   + "Clients:\n\t- Mauricio\n"
                                                   + "Invited clients:\n\t- Mauricio")

    def test_str_private_empty(self):
        self.private_room.remove_client(self.client)
        self.assertEqual(self.private_room.__str__(),"Private room name: foo\n"
                                                   + "Room owner: Mauricio\n"
                                                   + "There's no clients in the room.\n"
                                                   + "Invited clients:\n\t- Mauricio")

    def test_get_room_owner(self):
        self.assertIs(self.private_room.get_room_owner(),self.client)

    def test_get_room_name(self):
        self.assertEqual(self.public_room.get_room_name(),"public_room")

    def test_room_is_public(self):
        self.assertEqual(self.public_room.room_is_public(),True)

    def test_set_room_owner(self):
        self.private_room.set_room_owner(self.client2)
        self.assertEqual(self.private_room.room_owner,self.client2)

    def test_set_room_name(self):
      self.private_room.set_room_name("bar")
      self.assertEqual(self.private_room.room_name,"bar")

    def test_invite_client_public_room(self):
        with self.assertRaises(customexceptions.PublicRoomException):
            self.public_room.invite_client(self.client2,self.client)

    def test_invite_client_not_owner(self):
        with self.assertRaises(customexceptions.InviterClientIsNotOwnerException):
            self.private_room.invite_client(self.client2,self.client2)

    def test_invite_client__client_already_invited(self):
        self.private_room.invite_client(self.client2,self.client)
        with self.assertRaises(customexceptions.ClientAlreadyInvitedException):
            self.private_room.invite_client(self.client2,self.client)

    def test_invite_client(self):
        self.private_room.invite_client(self.client2,self.client)
        self.assertIs(self.private_room.invited_clients.pop(),self.client2)

    def test_add_client_already_in_room(self):
        self.public_room.add_client(self.client)
        with self.assertRaises(customexceptions.ClientAlreadyInRoomException):
            self.public_room.add_client(self.client)

    def test_add_client_public_room(self):
        self.public_room.add_client(self.client)
        self.assertIs(self.public_room.room_clients.pop(),self.client)

    def test_add_client_not_invited(self):
        with self.assertRaises(customexceptions.NotInvitedClientException):
            self.private_room.add_client(self.client2)

    def test_add_client_private_room(self):
        self.private_room.invite_client(self.client2,self.client)
        self.private_room.add_client(self.client2)
        self.assertIs(self.private_room.room_clients.pop(),self.client2)
        self.assertEqual(len(self.private_room.invited_clients),1)

    def test_remove_nonexistet_client(self):
        with self.assertRaises(customexceptions.NonexistentClientException):
            self.public_room.remove_client(self.client)

    def test_remove_client(self):
        self.public_room.add_client(self.client)
        self.public_room.remove_client(self.client)
        self.assertEqual(not self.public_room.room_clients,True)

    def test_verify_name(self):
        self.public_room.add_client(self.client)
        with self.assertRaises(customexceptions.ExistingUsernameException):
            self.public_room.verify_name("Mauricio")

if __name__ == '__main__':
    unittest.main()
