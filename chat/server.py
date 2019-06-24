#! /usr/bin/env python

import json
import socket as sk
import threading
import time

import Pyro4
from chat_service import Chat


class Lobby:
    def __init__(self, hostname='localhost', port=25501):
        self.chats = []
        self.daemon = Pyro4.Daemon(host=hostname, port=port)

    def daemon_loop(self):
        self.d_thread = threading.Thread(
            target=self.daemon.requestLoop
        )

        self.d_thread.daemon = True
        self.d_thread.start()

    def register(self, chat_p=None):
        if isinstance(chat_p, str):
            chat_p = Chat(name=chat_p)
            self.register(chat_p)
        elif chat_p is None:
            chat_p = Chat()
            self.register(chat_p)

        elif isinstance(chat_p, Chat):
            uri = str(self.daemon.register(chat_p))
            self.chats.append((chat_p.name, uri))


class Server():
    def __init__(self, hostname='localhost', port=25500, lobby_port=25501):
        """
        This class works as a DNS server for the chats
        """

        self.lobby = Lobby(
            hostname=hostname,
            port=lobby_port
        )

        self.lobby.daemon_loop()

        self._server = sk.socket(
            sk.AF_INET,
            sk.SOCK_STREAM
        )

        self._server.bind((hostname, port))

    def run(self):
        self.s_thread = threading.Thread(target=self._run)
        self.s_thread.daemon = True
        self.s_thread.start()

    def _run(self):
        self._server.listen()

        while True:
            con, cliente = self._server.accept()
            mensagem = con.recv(2048).decode('utf-8')

            if mensagem == 'GET uri':
                con.send(json.dumps(self.lobby.chats).encode())

            con.close()

    def create_chat(self, chat_name):
        self.lobby.register(chat_name)


if __name__ == "__main__":
    server = Server()

    print('Server is running ...')

    server.create_chat('Pokoj 1')
    server.create_chat('Pokoj 2')
    server.create_chat('Pokoj 3')
    server.run()

    while True:
        time.sleep(30)
