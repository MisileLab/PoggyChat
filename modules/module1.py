import socket
import threading
import tomli

# GUI import
from PySide6.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QTextEdit
from PySide6.QtWidgets import QPushButton

import sys


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
                print(f"shutdown socket {address}")
                client.shutdown(socket.SHUT_RDWR)

            send_thread = threading.Thread(target=self.only_socket_send_message, args=(client, ))
            send_thread.start()
            while True:
                msg = client.recv(1024).decode('utf-8')
                print(f'{address[0]}: {msg}')
                if (not msg):
                    break

    def receive_message(self, ip: int, port: int):
        print(f'Run server using {port} port.')
        if self.server is None:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen()
        del(self.receive_thread)
        self.receive_thread = threading.Thread(target=self.receive_message_none_threading)
        self.receive_thread.start()

    def send_message_none_threading(self, address: str, port: int):
        self.sendsocket.connect((address, port))
        print("Can send now")
        send_thread = threading.Thread(target=self.only_socket_receive_message, args=(self.sendsocket,))
        send_thread.start()
        while True:
            msg = input("me: ")
            self.sendsocket.send(msg.encode('utf-8'))

    def send_message(self, address: str, port: int):
        print(f'Connect to {address}:{port}')
        if self.sendsocket is None:
            self.sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        del(self.send_thread)
        self.send_thread = threading.Thread(target=self.send_message_none_threading, args=(address, port,))
        self.send_thread.start()

    @staticmethod
    def only_socket_send_message(client: socket.socket):
        while True:
            msg = input("me: ")
            client.send(msg.encode('utf-8'))

    @staticmethod
    def only_socket_receive_message(client: socket.socket):
        while True:
            message = client.recv(1024).decode('utf-8')
            address = client.getsockname()[0]
            print(f"{address}: {message}")


class PoggyChatGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setupui()

    def setupui(self):

        # Set chat screen
        self.setBaseSize(206, 206)
        self.setWindowTitle("PoggyChat")
        self.chathbox = QHBoxLayout()
        self.typechathbox = QHBoxLayout()
        self.chatvbox = QVBoxLayout()
        self.chatscreen = QTextEdit()
        self.chatbutton = QPushButton('connect')
        self.chatting = QLineEdit()
        self.screenpoggyipport = PoggyChatConnectIPPort()
        self.chatbutton.clicked.connect(self.screenpoggyipport.setui)

        self.chatscreen.setReadOnly(True)

        self.typechathbox.addWidget(self.chatting)
        self.typechathbox.addWidget(self.chatbutton)

        self.chathbox.addStretch(1)
        self.chathbox.addWidget(self.chatscreen, stretch=100)
        self.chathbox.addStretch(1)

        self.chatvbox.addStretch(10)
        self.chatvbox.addLayout(self.chathbox, stretch=100)
        self.chatvbox.addStretch(5)
        self.chatvbox.addLayout(self.typechathbox)
        self.chatvbox.addStretch(6)

        # final layout set
        self.setLayout(self.chatvbox)


class PoggyChatConnectIPPort(QDialog):
    def setui(self):
        self.setFixedSize(220, 100)

        self.ipedit = QLineEdit()
        self.portedit = QLineEdit()
        self.iptext = QLabel("ip")
        self.porttext = QLabel("port")
        self.connectbutton = QPushButton('connect')

        self.screenvbox = QVBoxLayout()
        self.screenhbox = QHBoxLayout()
        self.screenhbox2 = QHBoxLayout()
        self.screenhbox3 = QHBoxLayout()

        self.screenhbox.addWidget(self.iptext, stretch=5)
        self.screenhbox.addWidget(self.porttext, stretch=5)

        self.screenhbox2.addWidget(self.ipedit, stretch=5)
        self.screenhbox2.addWidget(self.portedit, stretch=5)

        self.screenhbox3.addWidget(self.connectbutton, stretch=5)

        self.screenvbox.addLayout(self.screenhbox, stretch=30)
        self.screenvbox.addLayout(self.screenhbox2, stretch=30)
        self.screenvbox.addLayout(self.screenhbox3, stretch=50)

        self.setLayout(self.screenvbox)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pogchat = PoggyChatGUI()
    pogchat.show()
    sys.exit(app.exec())
