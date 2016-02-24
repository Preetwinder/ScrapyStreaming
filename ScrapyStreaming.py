#!/usr/bin/python2

import sys

from twisted.internet.defer import Deferred
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

from StreamingSpider import StreamingSpider
from LineReceiverProcess import Communicate
from Utils import deserializeLine


class ScrapyStreaming():

    def __init__(self, cmd):
        cmd = cmd.split()
        self.process = Communicate()
        dfd = Deferred()
        dfd.addCallback(deserializeLine)
        dfd.addCallback(self.generateSpider)
        dfd.addCallback(self.runSpider)
        reactor.callLater(0, self.process.start, cmd)
        reactor.callLater(0, self.process.get, dfd)
        reactor.run()

    def generateSpider(self, settings):
        class Spider(StreamingSpider):
            name = settings['name']
            process = self.process
            allowed_domains = settings['allowed_domains']
            start_urls = settings['start_urls']
        return Spider

    def runSpider(self, spider):
        configure_logging({'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s'})
        settings = Settings()
        settings.set('FEED_URI', 'output.json')
        settings.set('FEED_FORMAT', 'json')
        
        runner = CrawlerRunner(settings)
        dfd = runner.crawl(spider)
        dfd.addBoth(lambda _: reactor.stop())


if __name__ == '__main__':
    ScrapyStreaming(sys.argv[1])
