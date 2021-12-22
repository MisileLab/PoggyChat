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
parser.add_argument('--receive', required=False, default=False, type=bool,
                    help="true = first-receive mode, false = first-send mode")
args = parser.parse_args()

if args.receive == args.send:
    raise ValueError("receive and send arg values are same.")
receive = args.receive is True

a = md1.PoggyChatClient()

if receive:
    a.receive_message(args.ip, args.port)
else:
    a.send_message(args.ip, args.port)
