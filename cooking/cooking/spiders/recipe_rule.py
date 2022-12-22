import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

"""
1- Pegar receitas
    1.a - Info:
        Nome Receita, (str)
        Descrição, (str)
        Avaliação, (str)
        Tempo de Preparo, (str - num)
        Tempo de Fogão/Forno, (str - num)
        Tempo Total, (str - num)
        Categoria, (str)
        Cozinha, (str)
        Porções, (str - num)
        Calorias, (str - num)
    1.b - Info 2:
        Ingredientes, (list)
        Modo de preparo (str)
        Dicas, (str)
        URL, (str)
        Img, (ing)

2- Mexer em Settings, Middlewares e Pipelines (conectar com um banco)
3- Tentar utilizar Selenium/Splash
4- Enviar para e-mail (Opcional)
"""

class RecipeRuleSpider(CrawlSpider):
    name = 'recipe_rule'
    allowed_domains = ['cooknenjoy.com']
    start_urls = ['https://cooknenjoy.com/']
    # start_urls = ['https://cooknenjoy.com/category/receita/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article[contains(@class, "simple-grid")]/a'), callback='parse_item', follow=True),
        # Tentando percorrer pelas páginas com RUle
        Rule(LinkExtractor(restrict_xpaths='//a[@class="more-link ml-c"]')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pagination-next alignright"]/a')),
    )
    # Tentando percorrer página com forma padrão do Scrapy
    # nextPage = response.xpath('//div[contains(@class, "alignright")]/a/@href').get()
    # if nextPage:
    #     yield scrapy.Request(url=nextPage, callback=self.parse)

    def parse_item(self, response):
        # Informações gerais da receita
        # Pegando o tempo e formatando para se tornar uma string
        preparation_time = response.xpath('//div[contains(@class, "wprm-recipe-prep-time-container")]/span[2]/span/text()').getall()
        stove_time = response.xpath('//div[contains(@class, "wprm-recipe-cook-time-container")]/span[2]/span/text()').getall()
        total_time = response.xpath('//div[contains(@class, "wprm-recipe-total-time-container")]/span[2]/span/text()').getall()
        preparation_time_format = ''.join(preparation_time)
        stove_time_format = ''.join(stove_time)
        total_time_format = ''.join(total_time)

        # Incrementação de duas listas, uma com valor e outra com tipo de unidade
        amount_calories = response.xpath('//span[contains(@class, "wprm-recipe-nutrition-with-unit")]/span[1]/text()').get()
        calories_unit = response.xpath('//span[contains(@class, "wprm-recipe-nutrition-with-unit")]/span[2]/text()').get()
        calories = f'{amount_calories}{calories_unit}'

        # Pegando outros valores para a spider que não precisam de um tratamento/cálculo específico
        title = response.xpath('//h2[contains(@class, "wprm-recipe-name wprm-block-text-bold")]/text()').get()
        description = response.xpath('//div[contains(@class, "wprm-recipe-summary wprm-block-text-normal")]/span/text()').get()
        category = response.xpath('//div[contains(@class, "wprm-recipe-course-container")]/span[2]/text()').get()
        kitchen = response.xpath('//div[contains(@class, "wprm-recipe-cuisine-container")]/span[2]/text()').get()
        portion = response.xpath('//div[contains(@class, "wprm-recipe-servings-container")]/span[2]/text()').get()

        # Informações para a realização da receita
        equipment = response.xpath('//a[contains(@class, "wprm-recipe-equipment-link")]/text()').getall()
        preparation_method = response.xpath('//div[contains(@class, "wprm-recipe-instruction-text")]/text()').getall()
        tips = response.xpath('//div[contains(@class, "wprm-recipe-notes")]/span[2]/text()').getall()
        # url = response.xpath('').get()
        image = response.xpath('//div[contains(@class, "wprm-recipe-notes")]/span/img/@src').getall()

        yield {
            'Title': title,
            'Description': description,
            # 'rating': response.xpath('').get(),
            'Preparation time': preparation_time_format,
            'Stove time': stove_time_format,
            'Total time': total_time_format,
            'Category': category,
            'Kitchen': kitchen,
            'Portion': portion,
            'Calories': calories,
            'Others': {
                'Equipment': equipment,
                'Preparation method': preparation_method,
                'Tips': tips,
                # 'URL': url,
                'Image': image,
            }
        }