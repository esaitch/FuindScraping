# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class VeluxCovidSpider(scrapy.Spider):
    name = 'veluxcovid'
    pid = '08'
    start_id = 1
    allowed_domains = ['veluxfoundations.dk']
    start_urls = ['https://veluxfoundations.dk/en/content/humanities-and-social-scientists-document-impact-covid-19-crisis']

    def parse(self, response):
        for project in response.xpath('//div[@id="block-system-main"]/article/article[4]/div/p'):
            name_title = project.xpath('./strong/text()').extract_first().strip()
            titles = ['associate professor', 'head of research', 'professor']
            for t in titles:
                if t in name_title.lower():
                    title = t
                    name = name_title.lower().replace(t, '').strip().title()
                    break

            info = project.xpath('./text()').extract_first()

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name,
                co_pi=None,
                pi_affiliation=re.findall(r', (.*): ‘', info)[0],
                gender=None,
                career_stage=title,
                country_of_origin=None,
                funder='Velux',
                grant_programme=None,
                title=re.findall(r'‘(.*)’', info)[0],
                summary=None,
                award_application_date=None,
                start_date=None,
                end_date=None,
                amount_awarded=re.findall(r'\d+', re.findall(r'\((.*)\)', info)[0].replace(',', ''))[0],
                research_area=None,
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=1,
            )

            # increase id for next project
            self.start_id += 1

