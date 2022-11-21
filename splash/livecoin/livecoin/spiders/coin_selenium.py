import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which

class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['web.archive.org']
    start_urls = [
        'https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/'
    ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headles')

        chrome_path = which('chromedriver')

        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get('https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/')

        rur_tab = driver.find_element_by_class_name('filterPanelItem___2z5Gb')
        rur_tab[4].click()

        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for currency in resp.xpath('//div[(@class="tableRow___3EtiS ")]'):
            yield {
                'currency pair': currency.xpath('.//div[1]/div/text()').get(),
                'volume(24)': currency.xpath('.//div[2]/span/text()').get(),
            }