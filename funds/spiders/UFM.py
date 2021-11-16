# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class UFMSpider(scrapy.Spider):
    name = 'ufm'
    pid = '26'
    start_id = 1
    start_urls = ['https://ufm.dk/forskning-og-innovation/tilskud-til-forskning-og-innovation/hvem-har-modtaget-tilskud/2020',
                  'https://ufm.dk/forskning-og-innovation/tilskud-til-forskning-og-innovation/hvem-har-modtaget-tilskud/2021']

    def parse(self, response):
        for grant in response.xpath('//div[@id="advanced-results"]/dl/dt//a/@href').extract():
            yield scrapy.Request(url=grant, callback=self.parse_projects)

    def parse_projects(self, response):
        grant_info = response.xpath('//h1/text()').extract_first()
        year = re.findall(r'\d{4}', grant_info)[0]
        grant = grant_info.replace(year, '').split('-')[0].strip()

        for project in response.xpath('//div[@id="parent-fieldname-text"]/hr/following-sibling::p'):
            if not (title := project.xpath('./strong/text()').extract_first()):
                title = project.xpath('.//text()[1]').extract_first().split(':')[-1]

            recipient = project.xpath('./text()[contains(.,"Bevillingsmodtager")]').extract_first()
            if not recipient or not recipient.strip():
                continue

            career_list = ['Associate Professor', 'Clinical professor', 'Professor', 'Specialkonsulent', 'Senior researcher', 'Lektor', 'Consultant']
            career = next((c for c in career_list if c.lower() in recipient.lower()), None)

            name = recipient.split(':')[-1].strip()
            if career:
                name = name.replace(career, '')

            if place := project.xpath('./text()[contains(.,"Institution")]').extract_first():
                place = place.split(':')[-1].strip()
            if 'universitet' in name.lower():
                place = name
                name = None

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name.strip().rstrip(',') if name else None,
                co_pi=None,
                pi_affiliation=place,
                gender=None,
                career_stage=career,
                country_of_origin=None,
                funder='UFM',
                grant_programme=grant,
                title=title.strip(),
                summary=None,
                award_application_date=year,
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'\d+', project.xpath('./text()[contains(.,"eløb")]').extract_first().replace('.', ''))[0]),
                research_area=project.xpath('./text()[contains(.,"Fagområde")]').extract_first().split(':')[-1].strip() if
                                project.xpath('./text()[contains(.,"Fagområde")]').extract_first() else None,
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0,
            )

            self.start_id += 1
