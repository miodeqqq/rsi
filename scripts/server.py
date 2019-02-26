#! /usr/bin/env python

import Pyro4


class Calculator:
    def mul(self, x, y): return x * y

    def sub(self, x, y): return x - y

    def add(self, x, y): return x + y

    def div(self, x, y): return x / y


@Pyro4.expose
class GreetingsServer(Calculator):
    """
    Anything that isn’t decorated with @expose is not remotely accessible.
    Thanks to decorator it allows to mark classes/methods/properties to be available for remote access.
    """

    def __init__(self):
        super(GreetingsServer, self).__init__()

    def get_name(self, name):
        return 'Hello, {0}.'.format(name)

    def run_server(self):
        # creates a Pyro daemon

        with Pyro4.core.Daemon() as daemon:
            # Greetings as Pyro object
            uri = daemon.register(GreetingsServer, 'calculator')

            calculator = Calculator()

            daemon.register(calculator)

            # print the uri so we can use it in the client later
            print('[Server is running] Object URI --> {}'.format(uri))

            # start the event loop of the server to wait for calls
            daemon.requestLoop()


GreetingsServer().run_server()
