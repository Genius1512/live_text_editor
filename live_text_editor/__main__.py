from sys import argv
from client import *
from server import *
from argparse import ArgumentParser


def main():

    parser = ArgumentParser(
        description="Live Text Editor"
    )
    parser.add_argument(
        "mode",
        help="Server or client"
    )
    parser.add_argument(
        "--ip",
        default=config.config["standard_ip"],
        required=False,
        help="IP to connect to"
    )
    parser.add_argument(
        "--port",
        default=config.config["standard_port"],
        type=int,
        help="Port to connect to/Port o setup server on"
    )
    parser.add_argument(
        "--file",
        default=config.config["default_file"],
        required=False,
        help="File to edit"
    )
    args = parser.parse_args()

    if args.mode == "server":
        server = Server(
            file=args.file,
            port=args.port
        )

    elif args.mode == "client":
        client = Client(
            ip=args.ip,
            port=args.port
        )

    else:
        print(f"Invalid mode {args.mode}")


if __name__ == "__main__":
    main()