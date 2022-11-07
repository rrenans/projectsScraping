import scrapy

# https://www.glassesshop.com/bestsellers

class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    # def start_requests(self):
    #     yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
    #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    #     })

    def parse(self, response):
        for glasses in response.xpath('//div[contains(@class, "product-list-item")]'):
            yield {
                'product_url': glasses.xpath('.//div[@class="product-img-outer"]/a/@href').get(),
                'product_image_link': glasses.xpath('.//div[@class="product-img-outer"]/a/img/@data-src').get(),
                'product_name': glasses.xpath('.//div[@class="p-title"]/a/text()').get().strip(),
                'product_price': glasses.xpath('.//div[@class="p-price"]/div/span/text()').get().strip(),
                # 'User-Agent': response.request.headers['User-Agent'],
            }

        nextPage = response.xpath('//ul[contains(@class, "pagination")]/li[6]/a/@href').get()
        if nextPage:
            yield scrapy.Request(url=nextPage, callback=self.parse)
            # yield scrapy.Request(url=nextPage, callback=self.parse, headers={
            #     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
            # })
