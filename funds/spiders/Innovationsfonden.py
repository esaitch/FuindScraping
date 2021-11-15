# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class InnovationsfondenSpider(scrapy.Spider):
    name = 'innovationsfonden'
    pid = '22'
    start_id = 1
    allowed_domains = ['innovationsfonden.dk']
    start_urls = ['https://innovationsfonden.dk/da/investeringer/investeringsoversigt?field_program_target_id=&field_start_year_value=2020&field_area_target_id=All&page=0',
                  'https://innovationsfonden.dk/da/investeringer/investeringsoversigt?field_program_target_id=&field_start_year_value=2021&field_area_target_id=All&page=0']

    def parse(self, response):
        for project in response.xpath('//td[@class="hidden"]'):
            period = project.xpath('./div[@class="period--text-hidden"]/text()').extract_first()

            amount = project.xpath('./div[@class="investment--value-hidden"]/text()').extract_first()

            if 'mio' in amount:
                string_int = re.findall(r'\d+(?:\.\d+)?', amount.replace(',', '.'))[0]
                amount = int(float(string_int) * 1000000)
            else:
                amount = int(amount.replace('.', ''))

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=None,
                co_pi=None,
                pi_affiliation=None,
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder='Innovationsfonden',
                grant_programme=project.xpath('./div[@class="program--text-hidden"]/text()').extract_first().strip(),
                title=project.xpath('./div[@class="title-hidden"]/text()').extract_first().strip(),
                summary=project.xpath('./div[@class="desscription"]/text()').extract_first(),
                award_application_date=re.findall(r'year_value=(\d{4})', response.url)[0],
                start_date=re.findall(r'\d{4}', period)[0],
                end_date=re.findall(r'\d{4}', period)[1],
                amount_awarded=amount,
                research_area=None,
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0,
            )

            self.start_id += 1

        if next_page := response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').extract_first():
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
