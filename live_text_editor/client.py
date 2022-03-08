from socket import *
from threading import Thread
import tkinter as tk
from time import sleep

import config
from console import *
from action import Action


class Client(socket):
    def __init__(self, args):
        # Client things
        self.ip = args.ip
        self.port = args.port

        # Socket things
        super(socket, self).__init__()
        spinner = Spinner("Connecting...")
        self.connect((self.ip, self.port))
        self.content = self.recv(1024).decode()
        spinner.stop()
        console.print("Connected", style="success")

        self.updater = Thread(
            target=self.update_text,
            daemon=True
        )
        self.updater.start()

        self.root = tk.Tk()
        self.root.title("Live Text Editor")
        self.root.geometry(f"{config.height}x{config.width}")
        self.root.configure(bg="#1e1e1e")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.text = tk.Text(
            self.root,
            height=config.height-20,
            width=config.width-20
        )
        self.text.configure(bg="#252527", fg="#9cdcfe", font=("Helvetica", 20))
        self.text.bind("<KeyPress>", self.on_key_press)
        self.text.pack()
        self.text.insert("0.0", self.content)

        self.selection_handler = Thread(
            target=self.handle_selection,
            daemon=True
        )
        self.selection_handler.start()

        self.root.mainloop()

    def update_text(self):
        while True:
            actions_str = self.recv(1024).decode()
            actions = actions_str.split(config.end_sep)
            for action_str in actions:
                if action_str == "exit":
                    console.print("Server closed", style="log")
                    self.root.destroy()
                elif action_str != "":
                    action = Action(action_str)
                    if action.char == "<-":
                        self.text.delete(action.pos+"-1c")
                    else:
                        self.text.insert(action.pos, action.char)

    def handle_selection(self):
        was_selected_last_time = False
        while True:
            if self.text.tag_ranges("sel") and not was_selected_last_time:
                print("Disable")
                self.text.configure(state="disabled")
            elif not self.text.tag_ranges("sel") and was_selected_last_time:
                print("Enable")
                self.text.configure(state="normal")
            was_selected_last_time = bool(self.text.tag_ranges("sel"))

    def on_key_press(self, event):
        if self.text.tag_ranges("sel"):
            return

        if event.keysym in ["Up", "Down", "Left", "Right"]:
            return
        if event.keysym == "Return":
            char = "\n"
        elif event.keysym == "BackSpace":
            if str(self.text.index(tk.INSERT)) != "1.0":
                char = "<-"
            else:
                return
        else:
            char = event.char
        self.send(f"{char}{config.sep}{self.text.index(tk.INSERT)}{config.end_sep}".encode())

    def on_close(self):
        self.send("exit".encode())
        self.root.destroy()
