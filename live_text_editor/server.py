from socket import *
from threading import Thread
from atexit import register
from functools import partial

import config
from action import Action
from console import *


# constants
SOCKET = 0
THREAD = 1


class Server(socket):
    def __init__(self, args):
        # Server things
        self.port = args.port
        self.max_connections = args.max
        self.file = args.file
        self.ip = gethostbyname(gethostname())

        # Load file content
        try:
            with open(self.file, "r") as f:
                self.content = f.read()
            if self.content == "":
                self.content = "Lorem ipsum dolor sit amet"
        except FileNotFoundError:
            with open(self.file, "w") as f:
                f.write("Lorem ipsum dolor sit amet")
            self.content = "Lorem ipsum dolor sit amet"

        # Socket things
        super(socket, self).__init__()
        self.bind(("0.0.0.0", self.port))
        self.listen(self.max_connections)
        console.print(f"Server online on {self.ip}:{self.port}", style="success")

        self.connections: dict[int, list[socket, Thread]] = {}
        for i in range(self.max_connections):
            self.connections[i] = [
                None,
                Thread(
                    target=self.handler,
                    args=(i,)
                )
            ]
        for conn in self.connections:
            self.connections[conn][THREAD].start()
        register(partial(self.on_close, self.connections))
        try:
            for conn in self.connections:
                self.connections[conn][THREAD].join()
        except KeyboardInterrupt:
            console.print("Press Ctrl+C again to quit")

    def handler(self, my_index):
        while True:
            self.connections[my_index][SOCKET] = self.accept()[0] # get connection
            console.print(f"{my_index} got connection", style="success")
            self.connections[my_index][SOCKET].send(self.content.encode())
            while True:
                actions_str = self.connections[my_index][SOCKET].recv(1024).decode()

                if actions_str == "exit":
                    self.connections[my_index][SOCKET].close()
                    self.connections[my_index][SOCKET] = None
                    break

                actions = actions_str.split(config.end_sep)
                for action_str in actions:
                    if action_str != "":
                        self.content = Action(action_str).insert_to_text(self.content)

                for conn_i in self.connections:
                    if conn_i != my_index and self.connections[conn_i][SOCKET]: self.connections[conn_i][SOCKET].send(actions_str.encode())
            console.print(f"{my_index} disconnected", style="success")
            print(self.content)

    def on_close(self, connections):
        for conn in connections:
            if connections[conn][SOCKET]:
                connections[conn][SOCKET].send(("exit"+config.end_sep).encode())
                connections[conn][SOCKET].close()

        with open(self.file, "w") as f:
            f.write(self.content)

    def __repr__(self):
        return f"Server on {self.ip}:{self.port}"
