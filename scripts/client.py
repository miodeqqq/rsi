#! /usr/bin/env python

import Pyro4
from Pyro4.errors import CommunicationError, PyroError


class GreetingsClient:
    uri, client_name, condition1, condition2 = None, None, False, False

    def get_uri_obj(self):
        self.uri = input('\n\tPlease put your URI object...\n')

        if not self.uri or not self.uri.strip():
            print('\tURI object string is required...\n')
        else:
            self.condition1 = True

    def get_client_name(self):
        self.client_name = input('\n\tWhat\'s your name ?\n')

        if not self.client_name or not self.client_name.strip():
            print('\tYour name is required...\n')
        else:
            self.condition2 = True

    def get_pyro_obj(self):
        if all([self.condition1, self.condition2]):
            # get pyro proxy obj
            try:
                greeting_server = Pyro4.Proxy(self.uri)

                # call method normally
                print('\tServer response --> {}\n'.format(greeting_server.get_name(self.client_name)))
            except CommunicationError:
                print('\tCannot connect to --> {}'.format(self.uri))
            except PyroError:
                print('\tInvalid URI...')

    def run(self):
        self.get_uri_obj()
        self.get_client_name()
        self.get_pyro_obj()


GreetingsClient().run()
