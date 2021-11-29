import socket
from dotenv import load_dotenv
import os
import argparse

import modules.module1 as md1

default_dotenv = """default_port=25564"""
md1.setup_file('.env', default_dotenv)
md1.setup_file('whitelist_clients.toml', 'whitelist_clients = ["192.168.0.1", "127.0.0.1"]')
load_dotenv(".env")
parser = argparse.ArgumentParser(description="This is PoggyChat.")

parser.add_argument('--port', required=False, default=int(os.getenv("default_port")), type=int,
                    help="Set Port, only number, need port when send mode")
parser.add_argument('--ip', required=True, type=str, help="Set the IP that send the socket")
parser.add_argument('--send', required=False, default=False, type=bool, help="Send Mode, Incompatible with Receive " +
                    "mode, bool type")
parser.add_argument('--receive', required=False, default=False, type=bool, help="Receive Mode, " +
                    "Incompatible With Send mode, bool type")
args = parser.parse_args()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if args.receive == args.send:
    raise ValueError("receive and send arg values are same.")
receive = args.receive is True
send = args.send is True

sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

a = md1.PoggyChatClient()
if receive:
    a.receive_message(args.ip, args.port)
elif send:
    a.send_message(args.ip, args.port)
