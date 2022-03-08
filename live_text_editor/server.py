from socket import *
from threading import Thread
from atexit import register

import config
from action import Action


# constants
SOCKET = 0
THREAD = 1


class Server(socket):
    def __init__(self, args):
        # Server things
        self.port = args.port
        self.max_connections = args.max
        self.file = args.file

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

        register(self.on_close)

        # Socket things
        super(socket, self).__init__()
        self.bind(("0.0.0.0", self.port))
        self.listen(self.max_connections)

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
        for conn in self.connections:
            self.connections[conn][THREAD].join()

    def handler(self, my_index):
        print(f"{my_index} started")
        while True:
            self.connections[my_index][SOCKET] = self.accept()[0] # get connection
            print(f"{my_index} got connection")
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
            print(f"{my_index} disconnected")

    def on_close(self):
        for conn in self.connections:
            if self.connections[conn][SOCKET]:
                self.connections[conn][SOCKET].send(("exit"+config.end_sep).encode())
                self.connections[conn][SOCKET].close()

        with open(self.file, "w") as f:
            f.write(self.content)

    def __repr__(self):
        return f"Server on {self.ip}:{self.port}"
