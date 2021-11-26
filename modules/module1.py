from socket import socket, SHUT_RDWR
import socket as socketer
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


def get_exist_in_list(data: list or dict, value) -> bool:
    """get value is exist or not exist in list, dict"""
    print(type(data))
    if type(data) == list:
        if data.index(value) > 0:
            return True
    elif type(data) == dict:
        for i in data.values():
            if i == value:
                return True
    return False


class PoggyChatClient:
    def __init__(self):
        setup_file("whitelist_clients.toml", 'whitelist_clients = ["192.168.0.1", "127.0.0.1"]')
        self.whitelist_clients = tomli.loads(open("whitelist_clients.toml", "r").read())["whitelist_clients"]
        self.server = None
        self.sendsocket = None
        self.receive_thread = None
        self.send_thread = None

    def receive_message_none_threading(self):
        while True:
            client, address = self.server.accept()
            if not get_exist_in_list(self.whitelist_clients, address[0]):
                print("shutdown socket {address}")
                client.shutdown(SHUT_RDWR)

            while True:
                msg = client.recv(1024).decode('utf-8')
                print("RECEIVE RESULT:", f'{address}: {msg}')
                if(not msg):
                    break

    def receive_message(self, ip: int, port: int):
        if self.server is None:
            self.server = socket(socketer.AF_INET, socketer.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen()
        del(self.receive_thread)
        self.receive_thread = threading.Thread(target=self.receive_message_none_threading)
        self.receive_thread.start()

    def send_message_none_threading(self, address: str, port: int):
        self.sendsocket.connect((address, port))
        print("can send now")
        while True:
            msg = input("me: ")
            self.sendsocket.send(msg.encode('utf-8'))

    def send_message(self, address: str, port: int):
        if self.sendsocket is None:
            self.sendsocket = socket(socketer.AF_INET, socketer.SOCK_STREAM)
        del(self.send_thread)
        self.send_thread = threading.Thread(target=self.send_message_none_threading, args=(address, port,))
        self.send_thread.start()
