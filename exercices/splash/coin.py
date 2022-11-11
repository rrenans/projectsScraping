import scrapy


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['web.archive.org']
    start_urls = ['http://web.archive.org/']

    def parse(self, response):
        pass
