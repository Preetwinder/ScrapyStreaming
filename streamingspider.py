import scrapy
from twisted.internet.defer import Deferred
from utils import deserializeLine, serializeObject


class StreamingSpider(scrapy.Spider):

    def parse(self, response):
        dfd = Deferred()
        dfd.addCallback(deserializeLine)
        self.process.getLine(dfd)
        self.process.sendLine(serializeObject(response))
        return dfd
