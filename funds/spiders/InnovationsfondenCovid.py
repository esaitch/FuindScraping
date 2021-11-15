# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class InnovationsfondenCovidSpider(scrapy.Spider):
    name = 'innovationsfondencovid'
    pid = '23'
    start_id = 1
    allowed_domains = ['innovationsfonden.dk']
    start_urls = ['https://innovationsfonden.dk/da/nyheder-presse-og-job/se-hvilke-covid-19-projekter-innovationsfonden-investerer-i']

    def parse(self, response):
        for project in response.xpath('//h2/following-sibling::p[contains(.,"Projektpart")]'):
            title = project.xpath('./preceding-sibling::p[1]/strong/text()').extract_first() or project.xpath('./preceding-sibling::p[2]/strong/text()').extract_first()
            place = project.xpath('./strong/following-sibling::text()[1]').extract_first() or project.xpath('./strong/text()').extract_first().split(':')[-1]

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=None,
                co_pi=None,
                pi_affiliation=place.strip(),
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder='Innovationsfonden',
                grant_programme=None,
                title=title.strip(),
                summary=project.xpath('./text()[1]').extract_first().strip(),
                award_application_date=None,
                start_date=None,
                end_date=None,
                amount_awarded=None,
                research_area=None,
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=1,
            )

            self.start_id += 1
