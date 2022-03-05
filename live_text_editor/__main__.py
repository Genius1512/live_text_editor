from sys import argv
from client import *
from server import *


def main(args):
    try:
        if args[1] == "server":
            server = Server()

        elif args[1] == "client":
            client = Client()

        else:
            print(f"Invalid mode {args[1]}")

    except IndexError:
        print("Not enough arguments")


if __name__ == "__main__":
    main(argv)