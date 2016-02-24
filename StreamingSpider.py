import scrapy
from twisted.internet.defer import Deferred
from Utils import deserializeLine, serializeObject


class StreamingSpider(scrapy.Spider):

    def parse(self, response):
        dfd = Deferred()
        dfd.addCallback(deserializeLine)
        self.process.get(dfd)
        self.process.send(serializeObject(response))
        return dfd
