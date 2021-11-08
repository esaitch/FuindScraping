# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class GigtforeningenSpider(scrapy.Spider):
    name = 'gigtforeningen'
    pid = '12'
    start_id = 1
    start_urls = ['https://www.gigtforeningen.dk/viden-om-gigt/forskning/forskningsuddelinger/']

    def parse(self, response):
        for project in response.xpath('//ul[@class="list accordion"]/li[1]/section/p'):
            header = project.xpath('./strong//text()').extract_first()
            split_header = header.rstrip(',').split(',')

            name_title = split_header[0]
            affil = split_header[1:]
            if len(name_title.split()) == 1:
                name_title = ','.join(split_header[:2])
                affil[3:]

            name = ' '.join(re.findall(r' ([A-ZÆØÅÜ][a-zæøåü]+)+', name_title)).strip()
            career = name_title.replace(name, '').strip()

            category = project.xpath('./preceding-sibling::h2[1]//text()').extract_first().strip()

            info = ''.join(project.xpath('.//text()').extract())
            info = info.replace(header, '').strip()

            title = re.findall(r'’(.*)’', info) or re.findall(r'‘(.*)’', info)
            title = title[0]

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name,
                co_pi=None,
                pi_affiliation=', '.join([s.strip() for s in affil if s.strip()]),
                gender=None,
                career_stage=career,
                country_of_origin=None,
                funder='Gigtforeningen',
                grant_programme=None,
                title=title,
                summary=re.findall(r'’(?:\.)? (.*)', info)[0].strip(),
                award_application_date='2020',
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'modtaget (\d+.\d+(?:\.\d+)?) kr', info)[0].replace('.', '')),
                research_area=category,
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0,
            )

            self.start_id += 1
