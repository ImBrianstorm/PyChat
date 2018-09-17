from chatclient import ChatClient

client = ChatClient("Mauricio","localhost",1234)
print(client)
print(client.getSocket())
