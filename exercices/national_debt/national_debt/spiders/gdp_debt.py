import scrapy

# https://worldpopulationreview.com/country-rankings/countries-by-national-debt

class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com']
    # start_urls = ['http://worldpopulationreview.com/']
    start_urls = ['https://worldpopulationreview.com/country-rankings/countries-by-national-debt']

    def parse(self, response):
        # countries = response.xpath("//table[contains(@class, 'tp-table-body')]/tbody/tr")
        # for country in countries:
        #     name = country.xpath(".//td[1]/text()").get()
        #     dbt = country.xpath(".//td[2]/text()").get()
        #     population = country.xpath(".//td[3]/text()").get()

        #     yield {
        #        'country_name': name,
        #        'gdp_debt': dbt,
        #        'population': population,
        #     }
       
       
        # rows = response.xpath("//table/tbody/tr")
        # for row in rows:
        #     yield {
        #         'country_name': row.xpath(".//td[1]/a/text()").get(),
        #         'gdp_debt': row.xpath(".//td[2]/text()").get()
        #     }
        pass