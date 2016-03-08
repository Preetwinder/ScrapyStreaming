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
        self.lrCallback(line)

    def send(self, line):
        self.sendLine(line)

    def connectionLost(self, reason):
        self.clCallback(reason)

class StreamingFactory(Factory):

    def __init__(self, lrCallback, clCallback):
        self.lrCallback = lrCallback
        self.clCallback = clCallback

    def buildProtocol(self, addr):
        sp = StreamingProtocol()
        sp.delimiter = '\n'
        sp.MAX_LENGTH = 10000000
        sp.lrCallback = self.lrCallback
        sp.clCallback = self.clCallback
        sp.dfds = []
        return sp


class Communicate():
    
    def start(self, cmd, lrCallback, clCallback):
        endpoint = DisconnectedWorkaroundEndpoint(ProcessEndpoint(reactor, 
                    'stdbuf', args = ['-o0', '-e0', '-i0'] + cmd)) 
        dfd = endpoint.connect(StreamingFactory(lrCallback, clCallback))
        dfd.addCallback(self.getProtocol)

    def getProtocol(self, protocolWrapper):
        self.protocol = protocolWrapper.wrappedProtocol

    def send(self, line):
        self.protocol.send(line)
