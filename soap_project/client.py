#! /usr/bin/env python

import logging

from suds.client import Client

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)


class DB:
    def __init__(self, url):
        self._client = Client(url)

    def send_values(self, values):
        """
        Creates a string array and sends data to server.
        """

        array_of_strings = self._client.factory.create('stringArray')

        array_of_strings.string.extend(values)

        self._client.service.write_values(array_of_strings)

    def receive_value(self, index):
        """
        Reads value with given index.
        """

        return self._client.service.read_value(index)


class SOAPClient:
    def __init__(self):
        self.client = DB(
            url='http://localhost:9000?wsdl'
        )

    def _send(self):
        values = [
            ['Maciej'],
            ['Januszewski'],
            ['RSI']
        ]

        self.client.send_values(values=values)

    def _read(self, index):
        response = self.client.receive_value(index)

        logging.info('\n\tRESPONSE FOR INDEX {index} --> {response}'.format(
            index=index,
            response=response
        ))

    def run(self):
        self._send()

        self._read(0)
        self._read(2)
        self._read(1)


c = SOAPClient()
c.run()
