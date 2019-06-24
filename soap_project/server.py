#! /usr/bin/env python

import logging
from wsgiref.simple_server import make_server

from rpclib.application import Application
from rpclib.decorator import srpc
from rpclib.model.complex import Array
from rpclib.model.primitive import Integer, String
from rpclib.protocol.soap import Soap11
from rpclib.server.wsgi import WsgiApplication
from rpclib.service import ServiceBase

logging.basicConfig(level=logging.DEBUG)

logging.getLogger('rpclib.protocol.xml').setLevel(logging.DEBUG)


class DB:
    _db = []

    @classmethod
    def write(cls, values):
        cls._db.extend(values)

    @classmethod
    def read(cls, index):
        return "" if len(cls._db) <= index else cls._db[index]


class RpcDbService(ServiceBase):
    @srpc(Array(String))
    def write_values(values):
        logging.info('VALUES TO WRITE --> {}'.format(values))
        DB.write(values)

    @srpc(Integer, _returns=String)
    def read_value(index):
        result = DB.read(index)

        logging.info('VALUE FOR INDEX {index} --> {value}'.format(index=index, value=result))

        return result


class SOAPServer:
    def __init__(self):
        self.app = Application(
            [RpcDbService],
            name='Miodek SOAP',
            tns='miodeq_ns',
            in_protocol=Soap11(validator='lxml'),
            out_protocol=Soap11()
        )

    def _runserver(self):
        host = 'localhost'

        port = 9000

        server = make_server(
            host=host,
            port=port,
            app=WsgiApplication(self.app)
        )

        server_url = 'http://{}:{}'.format(host, port)

        logging.info('\n\tListening to {server_url}'.format(server_url=server_url))

        logging.info('\n\tWSDL --> {wsdl_url}'.format(wsdl_url=server_url + '?wsdl'))

        server.serve_forever()

    def run(self):
        self._runserver()


s = SOAPServer()
s.run()
