import config
from socket import *
from threading import Thread
from atexit import register


class Server(socket):
    def __init__(self, file = config.config["default_file"], port = config.config["standard_port"]):
        # get file content
        try:
            with open(file, "r") as f:
                content = f.read()
        except FileNotFoundError:
            content = "Lorem ipsum dolor sit amet"
        self.file = file

        super().__init__()
        register(self.close)
        self.port = port

        self.bind(("0.0.0.0", self.port))
        self.listen(2)
        self.connections = {
            0: self.accept()[0],
            1: self.accept()[0]
        }
        print("Got connections")
        for conn in self.connections:
            print("Sending")
            self.connections[conn].sendall(content.encode())

        self.threads = [
            Thread(
                target=self.handler,
                args=(0,)
            ),
            Thread(
                target=self.handler,
                args=(1,)
            )
        ]
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

    def handler(self, my_index: int):
        other_index = not my_index
        while True:
            action = self.connections[my_index].recv(1024)
            if action.decode() == "Exiting":
                content = self.connections[my_index].recv(1024).decode()
                with open(self.file, "w") as f:
                    f.write(content)
                self.connections[my_index].close()
                del self.connections[my_index]
                break
            try:
                self.connections[other_index].send(action)
            except KeyError:
                pass
