import json
from socket import socket


def setup_file(filename: str, default_value: str):
    """
    if file is not exist, create file with default value.

    Params

    filename: str, filename that you want check.
    default_value: str, when file is not exist, this value will write in the created file.
    """
    try:
        open(filename)
    except FileNotFoundError:
        open(filename, 'w').write(default_value)


def get_exist_in_list(list: list or dict, value) -> bool:
    """get value is exist or not exist in list"""
    a = False
    if type(list) == list:
        for i in list:
            if i == value:
                a = True
                break
    elif type(list) == dict:
        for i in list.values():
            if i == value:
                a = True
                break
    return a


class PoggyChatClient:
    def __init__(self, server: socket):
        setup_file("whitelist_clients.json", "{}")
        self.whitelist_clients = json.loads(open("whitelist_clients.json", "r").read())
        self.server = server

    def receive_message(self):
        client, address = self.server.accept()
        if not get_exist_in_list(self.whitelist_clients, address):
            client.shutdown()
