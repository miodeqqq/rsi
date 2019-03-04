#! /usr/bin/env python

import sqlite3
import os
from Pyro4 import expose, Daemon


@expose
class GreetingsServer:
    """
    Anything that isn’t decorated with @expose is not remotely accessible.
    Thanks to decorator it allows to mark classes/methods/properties to be available for remote access.
    """

    def __init__(self):
        super(GreetingsServer, self).__init__()

        self.conn, self.cursor = self.db()

    def db(self):
        """
        Initialises connection with db (existing).
        """

        database = os.path.join('./rsi.db')

        conn = sqlite3.connect(
            database=database,
            timeout=5
        )

        return conn, conn.cursor()

    def get_name(self, name):
        return 'Hello, {0}.'.format(name)

    def get_products_count(self):
        """
        Returns products count.
        """

        products_count = self.cursor.execute("SELECT * from product;")

        return products_count.fetchone()[0]

    def get_persons_count(self):
        """
        Returns persons count.
        """

        for row in self.cursor.execute("SELECT * FROM person;"):
            print(row)

        persons_count = self.cursor.execute("SELECT * from person;")

        return persons_count.fetchone()[0]

    @staticmethod
    def mul(x, y):
        return x * y

    @staticmethod
    def sub(x, y):
        return x - y

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def div(x, y):
        return x / y

    def run_server(self):
        # creates a Pyro daemon
        with Daemon() as daemon:
            # Greetings as Pyro object
            uri = daemon.register(GreetingsServer, 'calculator')

            # print the uri so we can use it in the client later
            print('[Server is running] Object URI --> {}'.format(uri))

            # start the event loop of the server to wait for calls
            daemon.requestLoop()


GreetingsServer().run_server()
