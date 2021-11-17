import socket
from dotenv import load_dotenv

import modules.module1 as md1

default_dotenv = """default_server_port=25564"""
md1.setup_file('.env', default_dotenv)
md1.setup_file('whitelist_clients.json', '{}')

config = load_dotenv(".env")

server_port = config["default_server_port"]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind('127.0.0.1', server_port)
server.listen()

md1.server()
