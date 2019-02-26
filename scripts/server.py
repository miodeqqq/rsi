#! /usr/bin/env python

import Pyro4


class Calculator:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # multiple
    def __mul__(self):
        return self.x * self.y

    # substract
    def __sub__(self):
        return self.x - self.y

    # add
    def __add__(self):
        return self.x + self.y

    def __truediv__(self):
        return self.x / self.y


@Pyro4.expose
class GreetingsServer:
    """
    Anything that isn’t decorated with @expose is not remotely accessible.
    Thanks to decorator it allows to mark classes/methods/properties to be available for remote access.
    """

    def get_name(self, name):
        return 'Hello, {0}.'.format(name)

    def run_server(self):
        # creates a Pyro daemon
        daemon = Pyro4.Daemon()

        # Greetings as Pyro object
        uri = daemon.register(GreetingsServer, 'gretting')

        # print the uri so we can use it in the client later
        print('Object URI --> {}'.format(uri))

        # start the event loop of the server to wait for calls
        daemon.requestLoop()


GreetingsServer().run_server()
