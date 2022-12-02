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

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article[contains(@class, "simple-grid")]/a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # posso pegar o tempo e fazer um for
        tempo_preparo = response.xpath('//div[contains(@class, "wprm-recipe-prep-time-container")]/span[2]/span/text()').getall()
        # tempo_preparo[0,2]

        # tempo

        qtde_caloria = response.xpath('//span[contains(@class, "wprm-recipe-nutrition-with-unit")]/span[1]/text()').get()
        unidade_caloria = response.xpath('//span[contains(@class, "wprm-recipe-nutrition-with-unit")]/span[2]/text()').get()
        caloria = qtde_caloria + unidade_caloria


        yield {
            'title': response.xpath('//h2[contains(@class, "wprm-recipe-name wprm-block-text-bold")]/text()').get(),
            'description': response.xpath('//div[contains(@class, "wprm-recipe-summary wprm-block-text-normal")]/span/text()').get(),
            # 'rating': response.xpath('').get(),

            # gostaria de juntar os tempos em uma lista
            'tempo de preparo': tempo_preparo,
            # 'tempo de fogão': response.xpath('//div[contains(@class, "wprm-recipe-cook-time-container")]/span[2]/text()').get(),
            # 'tempo total': response.xpath('//div[contains(@class, "wprm-recipe-total-time-container")]/span[2]/text()').get(),

            # 'categoria': response.xpath('//div[contains(@class, "wprm-recipe-course-container")]/span[2]/text()').get(),
            # 'cozinha': response.xpath('//div[contains(@class, "wprm-recipe-cuisine-container")]/span[2]/text()').get(),

            # porções e calorias possuem dois valores, sendo a quantidade e o tipo (16kcal ou 16fatias)
            # gostaria de juntar os dois como uma lista, ou melhor, juntar os dois como um único valor
            # 'porções': response.xpath('//div[contains(@class, "wprm-recipe-servings-container")]/span[2]/text()').get(),
            # 'calorias': caloria,
        }
