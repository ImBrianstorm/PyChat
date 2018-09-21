from chatserver import ChatServer

if __name__ == '__main__':
  port = input("Puerto: ")
  if not port:
    port = 1234
  else:
    port = int(port)
  server = ChatServer(port=port)
  server.start_server()
  while server.is_connected():
    try:
      server.accept_client()
    except KeyboardInterrupt:
      break
  server.shutdown_server()
  print("\nServer apagado...")
