import scrapy


class QuotesInfoSpider(scrapy.Spider):
    name = 'quotes_info'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        pass
