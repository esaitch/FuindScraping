import scrapy
from funds.items.fundItem import FundItem

class TestSpider(scrapy.Spider):
    name = 'testspider'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/%22Hello,_World!%22_program']

    def _parse(self, response):
        yield FundItem(
            id=response.xpath('//h1/text()').extract_first().strip()
        )