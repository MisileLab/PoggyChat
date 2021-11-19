import socket
from dotenv import load_dotenv
import os

import modules.module1 as md1

default_dotenv = """default_server_port=25564"""
md1.setup_file('.env', default_dotenv)
md1.setup_file('whitelist_clients.json', '{}')

load_dotenv(".env")

server_port = int(os.getenv("default_server_port"))
server_port = int(input())
send_port = int(input('send'))
receiveorsend = input('receive or send')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', server_port))
server.listen()

sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

a = md1.PoggyChatClient(server, sendsocket)
if receiveorsend == "receive":
    a.receive_message()
else:
    a.send_message('127.0.0.1', send_port)
