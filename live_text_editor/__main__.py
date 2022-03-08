from argparse import ArgumentParser, ArgumentTypeError
import re

from exceptions import *
from client import Client
from server import Server
from console import *
import config


def ip(arg_value):
    pattern = re.compile("(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]){3}\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]))|localhost")
    if not pattern.match(arg_value):
        raise ArgumentTypeError(f"Invalid ip '{arg_value}'")
    return arg_value


# TODO: create port() function


def parse_args():
    parser = ArgumentParser(
        description = "Live Text Editor"
    )

    parser.add_argument(
        "mode",
        choices=["client", "server"],
        help="Client or Server"
    )
    parser.add_argument(
        "--ip",
        default=config.ip,
        type=ip,
        help="The IP to connect to"
    )
    parser.add_argument(
        "--port", "-p",
        default=config.port,
        type=int, # TODO: use type port()
        help="The port to connect to/to setup the server on"
    )
    parser.add_argument(
        "--file", "-f",
        default=config.file,
        help="The file to edit"
    )
    parser.add_argument(
        "--max","-m",
        default=config.max_connections,
        type=int,
        help="Maximal connections"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    if args.mode == "server":
        app = Server
    elif args.mode == "client":
        app = Client

    try:
        app(args)
    except Exception:
        console.print_exception()
        console.print("""Error when running Live Text Editor.
Please try again later or contact Silvan Schmidt""", style="error")


if __name__ == "__main__":
    main()
