# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool

class DanmarksFrieForskningsfondSpider(scrapy.Spider):
    name = 'dff'
    allowed_domains = ['dff.dk']
    start_urls = ['https://dff.dk/forskningsprojekter?SearchableText=&b_size:int=0&&filed_method:list=all&instrument:list=all&period:list=f0yb7m7qxl',
                  'https://dff.dk/forskningsprojekter?SearchableText=&b_size:int=0&&filed_method:list=all&instrument:list=all&period:list=yv0jhi0awh']

    '''
    We start by scraping the article listing all covid related projects that were funded.
    We get the titles of each of these. We remove all case distinction and full stops.
    
    We save these in a list. 
    Then we scrape the start_urls and remember to pass along the list of covid projects
    '''
    def start_requests(self):
        yield scrapy.Request(url='https://dff.dk/aktuelt/nyheder/dff-stotter-15-coronarelaterede-forskning-projekter', callback=self.parse_covid)

    def parse_covid(self, response):
        covid_projects = response.xpath('//p/a/u/text()').extract()
        covid_projects = [case.lower().replace('.', '').strip() for case in covid_projects]

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_projects, meta={'covid_projects': covid_projects})

    def parse_projects(self, response):
        '''
        We scrape all projects from 2020 and 2021

        grant_programme is set to scrape the field Virkemidler on the website
        award_application_date is simply the year - 2020 or 2021
        project_link is mainly just the main site (the overview). A few projects have a 'Læs case' link. In this case, this url will be scraped instead

        From the covid_projects list, we can fill in the covid_specific field by comparing the title of the projects.
        '''

        for project in response.xpath('//div[@class="result-item"]'):
            title = project.xpath('.//h2/a/text()').extract_first()

            all_projects = FundItem(
                id=ScrapingTool.hash_title(title),
                pi=project.xpath('.//h6[contains(.,"Modtager")]/following-sibling::div//strong/text()').extract_first().strip(),
                co_pi=None,
                pi_affiliation=project.xpath('.//h6[contains(.,"Modtager")]/following-sibling::div/br/following-sibling::text()').extract_first().strip(),
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder="Danmarks Frie Forskningsfond",
                grant_programme=project.xpath('.//ul[@class="listing-horizontal"]/li[1]/text()').extract_first().strip(),
                title=title,
                summary=project.xpath('./div[@class="row result-body"]/p/text()').extract_first(),
                award_application_date=project.xpath('.//ul[@class="listing-horizontal"]/li[3]/text()').extract_first().strip(),
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'\d+', response.xpath('.//h6[contains(.,"Bevilget beløb")]/following-sibling::div/div/text()').extract_first().replace('.', ''))[0]),
                research_area=project.xpath('.//ul[@class="listing-horizontal"]/li[2]/text()').extract_first().strip(),
                project_link=project.xpath('.//a[@class="result-link"][contains(.,"Læs case")]/@href').extract_first() or response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
            )

            all_projects['covid_specific'] = 0
            covid_projects = response.meta['covid_projects']
            if title.lower().replace('.', '').strip() in covid_projects:
                all_projects['covid_specific'] = 1

            yield all_projects