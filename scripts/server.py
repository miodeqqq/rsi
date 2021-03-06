#! /usr/bin/env python

import os
import sqlite3

from Pyro4 import expose, Daemon


@expose
class GreetingsServer:
    """
    Anything that isn’t decorated with @expose is not remotely accessible.
    Thanks to decorator it allows to mark classes/methods/properties to be available for remote access.
    """

    def __init__(self):
        super(GreetingsServer, self).__init__()

        self.conn, self.cursor = self.init_db()

    def init_db(self):
        """
        Initialises connection with db (existing).
        """

        database = os.path.join('./rsi.db')

        if os.path.isfile(database):
            conn = sqlite3.connect(
                database=database,
                timeout=5
            )

            return conn, conn.cursor()
        else:
            print('Database file not found...')
            exit()

    def get_name(self, name):
        """
        Returns username.
        """

        return 'Hello, {0}.'.format(name)

    def get_data_by_user_query(self):
        """
        Returns query result based on user input.
        """
        pass

    def get_products_count(self):
        """
        Returns products count.
        """

        return self.cursor.execute("SELECT count(*) from product;").fetchone()[0]

    def get_persons_count(self):
        """
        Returns persons count.
        """

        return self.cursor.execute("SELECT count(*) from person;").fetchone()[0]

    def get_all_products(self):
        """
        Returns all products data.
        """

        return self.cursor.execute("SELECT * FROM product;").fetchall()

    def get_all_persons(self):
        """
        Returns all persons data.
        """

        return self.cursor.execute("SELECT * FROM person;").fetchall()

    def get_by_query(self, user_query):
        """
        Querying db using text search
        """

        i_like = '%' + user_query + '%'

        product_search = "SELECT * FROM product WHERE name LIKE ? COLLATE NOCASE ORDER BY name;"

        person_search = "SELECT * FROM person WHERE name LIKE ? COLLATE NOCASE ORDER BY name;"

        _result_a = self.cursor.execute(product_search, (i_like,)).fetchall()

        _result_b = self.cursor.execute(person_search, (i_like,)).fetchall()

        _result_a.extend(_result_b)

        return _result_a

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

            with open('./uri.txt', 'w') as f:
                f.write(str(uri).strip())

            print('[Server is running] Object URI --> {}'.format(uri))

            # start the event loop of the server to wait for calls
            daemon.requestLoop()


GreetingsServer().run_server()
