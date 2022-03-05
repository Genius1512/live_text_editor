import tkinter as tk
import config
from socket import *
from threading import Thread


class Client(tk.Tk):
    def __init__(self, ip: str = config.config["standard_ip"], port: int = config.config["standard_port"]):
        # Socket things
        self.ip = ip
        self.port = port

        self.socket = socket()
        self.socket.connect((self.ip, self.port))
        print("Connected")
        content = self.socket.recv(1024).decode()
        print("Content: " + content)

        # Threading things
        self.thread = Thread(
            target=self.update_text,
            daemon=True
        )
        self.thread.start()


        # Tkinter things
        super().__init__()
        self.title("Live Text Editor")
        self.geometry(config.windows_size_as_geometry())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.text = tk.Text(
            self,
            height=config.config["window_size"]["height"],
            width=config.config["window_size"]["width"]
        )
        self.text.pack()
        self.text.bind(
            "<KeyPress>",
            self.on_key_press
        )
        self.text.insert("0.0", content)

        self.mainloop()

    def update_text(self):
        while True:
            actions = self.socket.recv(1024).decode().split(config.config["end_sep"])
            for action in actions:
                action = actions.split(config.config["sep"])
                self.insert_text(action[0], action[1])


    def on_key_press(self, event):
        if event.keysym == "Return":
            action = f"\n{config.config['sep']}{self.text.index(tk.INSERT)}"
        elif event.keysym == "BackSpace":
            action = f"BackSpace{config.config['sep']}{self.text.index(tk.INSERT)}"
        else:
            action = f"{event.char}{config.config['sep']}{self.text.index(tk.INSERT)}"
        self.socket.send(action+config.config["end_sep"].encode())

    def on_close(self):
        self.socket.send("Exiting".encode())
        self.socket.send(self.text.get("0.0", "end").encode())
        self.destroy()

    def insert_text(self, char, pos):
        if char == "BackSpace":
            self.text.delete(pos+"-1c")
        else:
            self.text.insert(pos, char)
