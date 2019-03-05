#! /usr/bin/env python

import Pyro4


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Chat:
    def __init__(self, name=None):
        self._name = name
        self.messages = []
        self.users = {}
        self.usernames = []

    def connect(self, uri):
        """
        Initialises connection.
        """

        client = Pyro4.Proxy(uri)

        if uri in self.users or client.username in self.usernames:
            return False

        print('Client with with username ' + Colors.WARNING + '"{client_username}"'.format(
            client_username=client.username
        ) + Colors.ENDC + ' has connected.')

        self._send_message(f'{client.username} has joined the chat')

        # adding client to chat's users
        self.users[uri] = client

        self.usernames.append(client.username)

        if len(self.messages) < 21:
            return self.messages
        return self.messages[-20:]

    def disconnect(self, uri):
        """
        Method for remote uses to call when wants to disconnect from this chat.
        """

        # print(f"Disconnecting {self.users[uri].username}")

        print('Disconnecting ' + Colors.FAIL + '"{client_username}"'.format(
            client_username=self.users[uri].username
        ) + Colors.ENDC)

        self._send_message(f"User '{self.users[uri].username}' has disconnected.", uri)

        # clear the data:
        self.usernames.remove(self.users[uri].username)

        del (self.users[uri])

    def send_message(self, message, uri):
        if uri not in self.users:
            return

        sender = message.split(':')[0]

        if sender != self.users[uri].username:
            return

        self._send_message(message, uri)

    def _send_message(self, message, uri=None):
        self.messages.append(message)

        for user_uri, user in self.users.items():
            if user_uri == uri:
                continue

            user.incoming_message(message)

    def __str__(self):
        return f"Chat name has changed {self.name}"

    @property
    def name(self):
        return self._name
