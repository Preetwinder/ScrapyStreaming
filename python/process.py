from streaming import Comptroller
from scrapy.selector import Selector


base_url = '//div[@id="siteTable"]'


def parse(response):
    body = Selector(text=response['body'])
    lister = []
    for i in range(1, 51, 2):
        url  = base_url + '/div[' + str(i) + ']/div[2]/p/a'
        p = {}
        p['type'] = 'item'
        p['name'] = 'post'
        p['item'] = {}
        p['item']['title'] = body.xpath(url+'/text()').extract()[0]
        url = body.xpath(url+'/@href').extract()[0]
        p['item']['url'] = 'http://www.reddit.com' + url
        request = {'type':'request', 
                   'url':p['item']['url'], 
                   'callback':'get_content', 
                   'meta':{'item':p}}
        lister.append(request)
    return lister


def get_content(response): 
    p = response['meta']['item']
    doc = Selector(text=response['body'])
    content = doc.xpath(base_url+'/div/div/div/form/div/div/p/text()').extract()
    content = ''.join(content)
    p['item']['content'] = content
    return p


name = 'cscareerquestions'
start_urls = ['http://www.reddit.com/r/cscareerquestions']
allowed_domains = ['reddit.com']
Comptroller([parse, get_content], name, start_urls, allowed_domains)
