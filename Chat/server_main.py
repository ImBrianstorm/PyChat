from chatserver import ChatServer

if __name__ == '__main__':
  port = int(input("Puerto: "))
  server = ChatServer(port=port)
  server.start_server()
  listening = True
  while listening:
    try:
      server.accept_client()
    except KeyboardInterrupt:
      break
  server.shutdown_server()
  print("\nServer apagado...")
