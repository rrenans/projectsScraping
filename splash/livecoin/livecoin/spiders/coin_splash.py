import scrapy
from scrapy_splash import SplashRequest

class CoinSpider(scrapy.Spider):
    name = 'coin_splash'
    allowed_domains = ['web.archive.org']
    # start_urls = ['http://web.archive.org/']

    script = '''
        function main(splash, args)
            -- https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            rur_tab[5]:mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            return {
                image = splash:png(),
                html = splash:html(),
            }
        end
    '''
    def start_requests(self):
        yield SplashRequest(url='https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/', callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        for currency in response.xpath('//div[(@class="tableRow___3EtiS ")]'):
            yield {
                'currency pair': currency.xpath('.//div[1]/div/text()').get(),
                'volume(24)': currency.xpath('.//div[2]/span/text()').get(),
            }