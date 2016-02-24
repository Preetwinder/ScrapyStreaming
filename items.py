import scrapy


class post(scrapy.Item):
        title = scrapy.Field()
        content = scrapy.Field()
        url = scrapy.Field()
        
