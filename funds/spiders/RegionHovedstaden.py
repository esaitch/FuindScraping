# -*- coding: utf-8 -*-

import scrapy
import re
import pdfplumber

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class RegionHovedstadenSpider(scrapy.Spider):
    name = 'regionhovedstaden'
    pid = '11'
    start_id = 1
    start_urls = ['https://www.regionh.dk/til-fagfolk/Forskning-og-innovation/overblik-og-styrkepositioner/udvalgte-forskningsmiljoer/Stoettet-af-regionens-forskningsfond/Sider/Bevillingsmodtagere-2020.aspx']

    '''
    List of 2020 funded projects
    '''

    def parse(self, response):
        def clean_string(raw):
            no_line = re.sub('\r|\n', '', raw)
            single_space = re.sub(r' +', ' ', no_line)
            return single_space

        for project in response.xpath('//tbody/tr[position()>1]'):
            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=clean_string(project.xpath('./td[1]//strong/span/text()').extract_first().strip()),
                co_pi=None,
                pi_affiliation=clean_string(project.xpath('./td[3]//span/text()').extract_first()),
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder='Region Hovedstaden',
                grant_programme=None,
                title=clean_string(project.xpath('./td[2]//span/text()').extract_first()),
                summary=None,
                award_application_date='2020',
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'\d+', project.xpath('./td[5]//span/text()').extract_first().replace('.', ''))[0]),
                research_area=None,
                project_link=response.url,
                funded=1,
                amount_sought=int(re.findall(r'\d+', project.xpath('./td[4]//span/text()').extract_first().replace('.', ''))[0]),
                review_score=None,
                covid_specific=0,
            )

            self.start_id += 1
