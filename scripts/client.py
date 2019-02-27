#! /usr/bin/env python

import Pyro4
from Pyro4.errors import CommunicationError, PyroError


class GreetingsClient:
    uri, client_name, client_numbers, con1, con2, con3 = None, None, None, False, False, False

    pyro_obj = None

    def contain_only_numbers(self):
        """
        Checks whether the list contains only integers.
        """

        return all(x.isdigit() for x in self.client_numbers)

    def contain_only_two_numbers(self):
        """
        Checkse whether the list contains no more than 2 elements.
        """

        return True if len(self.client_numbers) == 2 else False

    def get_uri_obj(self):
        self.uri = input('\n\t1) Please put your URI object...\n\t')

        if not self.uri or not self.uri.strip():
            print('\n\tURI object string is required...\n\t')
        else:
            self.con1 = True

    def get_client_name(self):
        self.client_name = input('\n\t2) What\'s your name ?\n\t')

        if not self.client_name or not self.client_name.strip():
            print('\n\tYour name is required...\n')
        else:
            self.con2 = True

    def get_client_numbers(self):
        self.client_numbers = input('\n\t3) Put two (comma-separated numbers)...\n\t')

        if not self.client_numbers or not self.client_numbers.strip():
            print('\n\tNumbers are required...\n')

        self.client_numbers = [x.strip() for x in self.client_numbers.split(',')]

        if not self.contain_only_numbers():
            print('\n\tOnly integers are allowed...\n')

        elif not self.contain_only_two_numbers():
            print('\n\tOnly two numbers are allowed...\n')
        else:
            self.client_numbers = list(map(int, self.client_numbers))

            self.con3 = True

    def get_server_response_and_uri(self):
        """
        Returns server URI
        """

        print('\n\t3) Server response --> {}\n'.format(
            self.pyro_obj.get_name(self.client_name)
        ))

    def get_calculator_results(self):
        """
        Returns simple math results.
        """

        if self.uri:
            x, y = self.client_numbers
            print('\t4) Calculator results for numbers:\t')
            print('\t\ta) Sum: {}'.format(self.pyro_obj.add(x, y)))
            print('\t\tb) Substract: {}'.format(self.pyro_obj.sub(x, y)))
            print('\t\tc) Divide: {}'.format(self.pyro_obj.div(x, y)))
            print('\t\td) Multiple: {}'.format(self.pyro_obj.mul(x, y)))

    def get_pyro_obj(self):
        if all([self.con1, self.con2, self.con3]):
            try:
                with Pyro4.Proxy(self.uri) as obj:
                    self.pyro_obj = obj
            except CommunicationError:
                print('\t\nCannot connect to --> {}'.format(self.uri))

            except PyroError:
                print('\t\nInvalid URI...')

    def run(self):
        while not self.con1:
            self.get_uri_obj()

        while not self.con2:
            self.get_client_name()

        while not self.con3:
            self.get_client_numbers()

        self.get_pyro_obj()
        self.get_server_response_and_uri()
        self.get_calculator_results()


GreetingsClient().run()
