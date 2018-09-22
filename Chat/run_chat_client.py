from threading import Thread
import tkinter
from chatclient import ChatClient

if __name__ == '__main__':

    def receive():
      while True:
        try:
          message = client.receive_message()
          msg_list.insert(tkinter.END, message)
        except OSError:
          break

    def send(event=None):
        message = my_msg.get()
        my_msg.set("")
        client.send(message)
        if message == "DISCONNECT":
            client_socket.close()
            top.quit()

    def on_closing(event=None):
        client.send("DISCONNECT")
        client.close_socket()
        top.quit()


    host = input('Enter host: ')
    port = input('Enter port: ')
    if not host:
        host = "localhost"

    if not port:
        port = 1234
    else:
        port = int(port)

    client = ChatClient("Mauricio",host,port)
    client.init_socket()
    top = tkinter.Tk()
    top.title("PyChat: Chat built in Python")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()
    my_msg.set("")
    scrollbar = tkinter.Scrollbar(messages_frame)
    msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", activebackground="blue", activeforeground="white",
                                 background="yellow",command=send)
    send_button.pack(side=tkinter.TOP)

    top.protocol("WM_DELETE_WINDOW", on_closing)

    receive_thread = Thread(target=receive).start()
    tkinter.mainloop()
