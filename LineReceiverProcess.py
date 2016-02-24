from json import loads, dumps

from zope.interface import implementer
from twisted.internet.interfaces import IStreamClientEndpoint
from twisted.protocols.policies import WrappingFactory
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.endpoints import ProcessEndpoint

import scrapy


@implementer(IStreamClientEndpoint)
class DisconnectedWorkaroundEndpoint(object):
    def __init__(self, endpoint):
        self._endpoint = endpoint

    def connect(self, protocolFactory):
        return self._endpoint.connect(WrappingFactory(protocolFactory))


class StreamingProtocol(LineReceiver):

    def lineReceived(self, line):
        self.dfds.pop().callback(line)

    def send(self, line):
        self.sendLine(line)

    def setDeferred(self, dfd):
        self.dfds.append(dfd)


class StreamingFactory(Factory):

    def buildProtocol(self, addr):
        sp = StreamingProtocol()
        sp.delimiter = '\n'
        sp.MAX_LENGTH = 10000000
        sp.dfds = []
        return sp


class Communicate():
    
    def start(self, cmd):
        
        endpoint = DisconnectedWorkaroundEndpoint(ProcessEndpoint(reactor, 
                    'stdbuf', args = ['-o0', '-e0', '-i0'] + cmd)) 
        dfd = endpoint.connect(StreamingFactory())
        dfd.addCallback(self.getProtocol)

    def getProtocol(self, protocolWrapper):
        self.protocol = protocolWrapper.wrappedProtocol

    def send(self, line):
        self.protocol.send(line)

    def get(self, dfd):
        self.protocol.setDeferred(dfd)
