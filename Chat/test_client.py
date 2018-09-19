from chatclient import ChatClient
from socket import socket, AF_INET, SOCK_STREAM
import unittest

class TestClient(unittest.TestCase):

  def setUp(self):
    self.server = socket(AF_INET, SOCK_STREAM)
    address = ('',1234)
    self.server.bind(address)
    self.server.listen()

    self.client = ChatClient("Mauricio","localhost",1234)
    self.client.init_socket()

  def tearDown(self):
    self.client.close_socket()
    self.server.close()

  def test_str_connected(self):
    self.assertEqual(self.client.__str__(),"Mauricio -> localhost:1234 [CONNECTED]")

  def test_str_disconnected(self):
    self.client.close_socket()
    self.assertEqual(self.client.__str__(),"Mauricio -> localhost:1234 [DISCONNECTED]")

  def test_get_name(self):
    self.assertIs(self.client.get_name(),self.client.name)

  def test_get_host(self):
    self.assertIs(self.client.get_host(),self.client.host)

  def test_get_port(self):
    self.assertIs(self.client.get_port(),self.client.port)

  def test_get_address(self):
    self.assertIs(self.client.get_address(),self.client.address)

  def test_get_socket(self):
    self.assertIs(self.client.get_socket(),self.client.client_socket)

  def test_set_name(self):
    name = "Aglae"
    self.client.set_name(name)
    self.assertIs(name,self.client.name)

  def test_set_host(self):
    host = "127.0.0.8"
    self.client.set_host(host)
    self.assertIs(host,self.client.host)

  def test_set_port(self):
    port = 33000
    self.client.set_port(port)
    self.assertIs(port,self.client.port)

  def test_set_address(self):
    address = ("127.0.2.0",12345)
    self.client.set_address(address)
    self.assertIs(address,self.client.address)

  def test_set_socket(self):
    self.client.close_socket()
    newSocket = socket(AF_INET, SOCK_STREAM)
    address = ("127.0.0.1",1234)
    newSocket.connect(address)
    self.client.set_socket(newSocket)
    self.assertIs(newSocket,self.client.client_socket)

  def test_set_socket_None(self):
    socket = None
    self.client.set_socket(socket)
    self.assertIs(socket,self.client.client_socket)

if __name__ == '__main__':
  unittest.main()
