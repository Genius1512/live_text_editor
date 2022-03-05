import json


def get_config() -> dict:
    with open("config.json", "r") as f:
        return json.load(f)
config = get_config()

def windows_size_as_geometry() -> str:
    return f"{config['window_size']['height']}x{config['window_size']['width']}"