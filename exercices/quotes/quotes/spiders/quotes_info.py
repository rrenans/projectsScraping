import scrapy
from scrapy_splash import SplashRequest

class QuotesInfoSpider(scrapy.Spider):
    name = 'quotes_info'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            splash:set_viewport_full()
            return {
                image = splash:png(),
                html = splash:html(),
            }
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js/', callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        for quotes in response.xpath('//div[@class="quote"]'):
            yield {
                'quote_text': quotes.xpath('.//span[@class="text"]/text()').get(),
                'author': quotes.xpath('.//span[2]/small/text()').get(),
                'tags': quotes.xpath('.//div[@class="tags"]/a/text()').getall(),
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            absolute_url = f"http://quotes.toscrape.com{next_page}"
            yield SplashRequest(url=absolute_url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })


        # DÚVIDA NISSO AQUI 
        # next_page = response.xpath('//li[@class="next"]/a/@href').get()
        # if next_page is not None:
        #     yield scrapy.Request(url=next_page, callback=self.parse)
        # yield scrapy.Request(response.urljoin(next_page), callback=self.parse)