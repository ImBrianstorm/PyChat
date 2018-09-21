from chatserver import ChatServer
from socket import socket, AF_INET, SOCK_STREAM
import unittest
from threading import Thread

class TestServer(unittest.TestCase):

  def setUp(self):
    self.server = ChatServer()
    self.server.start_server()

  def tearDown(self):
    self.server.shutdown_server()

  def test_str_connected(self):
    self.assertEqual(self.server.__str__(),"Server conectado en el puerto 1234")

  def test_str_disconnected(self):
    self.server.shutdown_server()
    self.assertEqual(self.server.__str__(),"Server desconectado")

  def test_is_connected(self):
    self.assertTrue(self.server.is_connected())

  def test_get_host(self):
    self.assertIs(self.server.get_host(),self.server.host)

  def test_get_port(self):
    self.assertIs(self.server.get_port(),self.server.port)

  def test_get_bufsize(self):
    self.assertIs(self.server.get_bufsize(),self.server.bufsize)

  def test_get_socket(self):
    self.assertIs(self.server.get_socket(),self.server.server_socket)

  def test_set_host(self):
    host = "127.0.0.8"
    self.server.set_host(host)
    self.assertIs(host,self.server.host)

  def test_set_port(self):
    port = 33000
    self.server.set_port(port)
    self.assertIs(port,self.server.port)

  def test_set_bufsize(self):
    bufsize = 2048
    self.server.set_bufsize(bufsize)
    self.assertIs(bufsize,self.server.bufsize)

  def test_set_socket(self):
    self.server.shutdown_server()
    new_socket = socket(AF_INET, SOCK_STREAM)
    address = ('127.0.0.1',1235)
    new_socket.bind(address)
    new_socket.listen()
    self.server.connected = True
    self.server.set_socket(new_socket)
    self.assertIs(new_socket,self.server.server_socket)

  def test_set_socket_None(self):
    socket = None
    self.server.set_socket(socket)
    self.assertIs(socket,self.server.server_socket)

if __name__ == '__main__':
    unittest.main()
