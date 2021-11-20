from socket import socket, SHUT_RDWR
import threading
import tomli


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
    def __init__(self, server: socket, sendsocket: socket):
        setup_file("whitelist_clients.toml", 'whitelist_clients = ["192.168.0.1"]')
        self.whitelist_clients = tomli.loads(open("whitelist_clients.toml", "r").read())["whitelist_clients"]
        self.server = server
        self.sendsocket = sendsocket
        self.receive_thread = None
        self.send_thread = None

    def receive_message_none_threading(self):
        while True:
            client, address = self.server.accept()
            if not get_exist_in_list(self.whitelist_clients, address):
                client.shutdown(SHUT_RDWR)

            print(client.recv(1024))

            msg = client.recv(1024).decode('utf-8')
            print(f'{address}: {msg}')

    def receive_message(self):
        del(self.receive_thread)
        self.receive_thread = threading.Thread(target=self.receive_message_none_threading)
        self.receive_thread.start()

    def send_message_none_threading(self, address: str, port: int):
        self.sendsocket.connect((address, port))
        while True:
            msg = input("me: ")
            self.sendsocket.send(msg.encode('utf-8'))

    def send_message(self, address: str, port: int):
        del(self.send_thread)
        self.send_thread = threading.Thread(target=self.send_message_none_threading, args=(address, port,))
        self.send_thread.start()
