import scrapy


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

class RecipeSpider(scrapy.Spider):
    name = 'recipe'
    allowed_domains = ['cooknenjoy.com']
    start_urls = ['https://cooknenjoy.com/']

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        yield {
            'title': title
        }