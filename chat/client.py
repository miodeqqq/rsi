#! /usr/bin/env python

import json
import socket as sk

from user import User


def get_uris(server, port):
    """
    Connects with DNS URI.
    """

    socket = sk.socket(
        sk.AF_INET,
        sk.SOCK_STREAM
    )

    socket.connect((server, port))

    socket.send('GET uri'.encode())

    serialized = socket.recv(4096).decode('utf-8')

    return json.loads(serialized)


def main(server='localhost', port=25500):
    while True:
        username = input('Username: ')

        if ':' not in username:
            break
        else:
            print("Username cannot contain ':' extra character...")

    uris = get_uris(server, port)

    while True:
        print('Available chat rooms:')

        for n, item in enumerate(uris):
            print(f"{n}: {item[0]}")

        selection = input("Select a chat room: ")

        try:
            uri = uris[int(selection)][1]
            break
        except (IndexError, ValueError):
            print(f"'{selection}' is not a valid chat, please, try again...")

    User(uri, username)


if __name__ == '__main__':
    main()
