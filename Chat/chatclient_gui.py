from tkinter import *

class ChatClientGUI(Frame):

    def __init__(self, master=None,exit_function=None,send_function=None,client=None):
        Frame.__init__(self, master)
        self.master = master
        self.exit_function = exit_function
        self.send_function = send_function
        self.client = client
        self.init_window()

    def init_window(self):
        self.gui_messages_frame = Frame(self.master)
        self.gui_message = StringVar()
        self.gui_scrollbar = Scrollbar(self.gui_messages_frame)
        self.gui_message_box = Listbox(self.gui_messages_frame, height=22, width=60, yscrollcommand=self.gui_scrollbar.set)
        self.gui_entry_field = Entry(self.master, textvariable=self.gui_message)
        self.gui_send_button = Button(self.master, text="Enviar", command=self.client_send)

        self.master.title("PyChat: Chat client built in Python")
        self.pack(fill=BOTH, expand=1)
        self.gui_scrollbar.pack(side=RIGHT, fill=Y)
        self.gui_message_box.pack(side=LEFT, fill=BOTH)
        self.gui_message_box.pack()
        self.gui_messages_frame.pack()
        self.gui_entry_field.bind("<Return>", self.client_send)
        self.gui_entry_field.pack()
        self.gui_send_button.pack()

    def client_exit(self):
        if self.exit_function is None:
            exit()
        else:
            self.exit_function(self.client)
            client.close_socket()
            exit()

    def client_send(self):
       if self.send_function is None:
           pass
       else:
           message = self.gui_message.get()
           self.gui_message.set("")
           self.send_function(message)
           if message == "DISCONNECT":
             exit()

    def get_gui_message_box(self):
        return self.gui_message_box

    def insert_on_gui_message_box(self,message):
        self.gui_message_box.insert(END, message)

if __name__=='__main__':
    root = Tk()
    root.geometry("400x300")
    app = ChatClientGUI(root)
    root.mainloop()
