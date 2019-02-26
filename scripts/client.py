#! /usr/bin/env python

import Pyro4
from Pyro4.errors import CommunicationError, PyroError


class GreetingsClient:
    uri, client_name, condition1, condition2 = None, None, False, False

    def get_uri_obj(self):
        self.uri = input('\n\t1) Please put your URI object...\n\t')

        if not self.uri or not self.uri.strip():
            print('\n\tURI object string is required...\n\t')
        else:
            self.condition1 = True

    def get_client_name(self):
        self.client_name = input('\n\t2) What\'s your name ?\n\t')

        if not self.client_name or not self.client_name.strip():
            print('\n\tYour name is required...\n')
        else:
            self.condition2 = True

    def get_pyro_obj(self):
        if all([self.condition1, self.condition2]):
            # get pyro proxy obj
            try:
                with Pyro4.Proxy(self.uri) as obj:
                    # call method normally
                    print('\n\t3) Server response --> {}\n'.format(
                        obj.get_name(self.client_name)
                    ))
            except CommunicationError:
                print('\t\nCannot connect to --> {}'.format(self.uri))

            except PyroError:
                print('\t\nInvalid URI...')

    def run(self):
        while not self.condition1:
            self.get_uri_obj()

        while not self.condition2:
            self.get_client_name()

        self.get_pyro_obj()


GreetingsClient().run()
