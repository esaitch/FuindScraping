# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class NovoNordisk(scrapy.Spider):
    name = 'novo'
    pid = '02'
    allowed_domains = ['novonordiskfonden.dk']
    start_urls = ['https://novonordiskfonden.dk/wp-admin/admin-ajax.php?language=da&action=fetch_bevillingslister_from_search&offset=0&c=308&f=year&s=desc']

    def parse(self, response):
        id = 1
        for project in response.xpath('//div[@class="nnf-grant-list__items"]/div'):
            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, id),
                pi=project.xpath('./div[1]/div/text()').extract_first(),
                co_pi=None,
                pi_affiliation=project.xpath('./div[2]/div[2]/text()').extract_first(),
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder='Novo Nordisk',
                grant_programme='Research in long-term health consequences of COVID-19 illness',
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
            id += 1