import scrapy


class RecipeSpider(scrapy.Spider):
    name = 'recipe'
    allowed_domains = ['cooknenjoy.com']
    start_urls = ['https://cooknenjoy.com/']

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        yield {
            'title': title
        }