# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class NovoNordiskCovid(scrapy.Spider):
    name = 'novocovid'
    pid = '02'
    start_id = 1
    allowed_domains = ['novonordiskfonden.dk']
    start_urls = ['https://novonordiskfonden.dk/wp-admin/admin-ajax.php?language=da&action=fetch_bevillingslister_from_search&offset=0&yf=2020&yt=2021&c=265&f=year&s=desc',
                  'https://novonordiskfonden.dk/wp-admin/admin-ajax.php?language=da&action=fetch_bevillingslister_from_search&offset=20&yf=2020&yt=2021&c=265&f=year&s=desc']

    def start_requests(self):
        # parse the first Research in long-term health consequences of COVID-19 illness projects
        yield scrapy.Request(url='https://novonordiskfonden.dk/wp-admin/admin-ajax.php?language=da&action=fetch_bevillingslister_from_search&offset=0&c=308&f=year&s=desc',
                             callback=self.parse, meta={'grant': 'Research in long-term health consequences of COVID-19 illness'})

        # Now parse the Støtte af projekter der søger at afbøde de sundhedsmæssige konsekvenser af coronavirus (COVID-19) epidemien i Danmark projects
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={'grant': 'Støtte af projekter der søger at afbøde de sundhedsmæssige konsekvenser af coronavirus (COVID-19) epidemien i Danmark'})

    def parse(self, response):
        for project in response.xpath('//div[@class="nnf-grant-list__item row single-grant"]'):
            name = project.xpath('./div[1]/div/text()').extract_first()
            place = project.xpath('./div[2]/div[2]/text()').extract_first()

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name.strip(),
                co_pi=None,
                pi_affiliation=(place or name).strip(),
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder='Novo Nordisk',
                grant_programme=response.meta['grant'],
                title=None,
                summary=project.xpath('./div[3]/div[2]/text()').extract_first(),
                award_application_date=project.xpath('./div[5]/div[2]/text()').extract_first().strip(),
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'\d+', project.xpath('./div[4]/div[@class="nnf-grant-list__info-text"]/text()').extract_first().replace('.', ''))[0]),
                research_area='Biomedical and Natural Sciences',
                project_link=None,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=1
            )

            self.start_id += 1

    '''
    Manual changes: Professor and Senior Staff Specialist - correct name is Anders Perner 
    '''