# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class NovoNordisk(scrapy.Spider):
    name = 'novo2'
    pid = '03'
    allowed_domains = ['novonordiskfonden.dk']
    start_urls = ['https://novonordiskfonden.dk/en/grants-awarded-for-projects-to-mitigate-the-adverse-health-effects-of-the-coronavirus-epidemic-in-denmark/']

    def parse(self, response):
        id = 1
        for project in response.xpath('//div[@class="nnf-simple-article__main-content js-table-of-contents__contents"]/p[position()>1]'):
            info = ' '.join([line.strip() for line in project.xpath('./strong/text()').extract()])
            if not info:
                continue

            place = re.findall(', (.*):', info)
            if not place:
                place = re.findall('– (.*):', info) if '–' in info else None

            title = info.split(place[0])[0].strip() if place else info.split(':')[0].strip()
            summ = project.xpath('./strong[position()=last()]/following-sibling::text()').extract_first()

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, id),
                pi=None,
                co_pi=None,
                pi_affiliation=place[0].strip() if place else None,
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder='Novo Nordisk',
                grant_programme=project.xpath('./preceding::h3[1]//text()').extract_first(),
                title=title.rstrip(','),
                summary=summ.strip() if summ else None,
                award_application_date=None,
                start_date=None,
                end_date=None,
                amount_awarded=re.findall(r'\d+', info.split(':')[-1].replace(',', ''))[0],
                research_area='Biomedical and Natural Sciences',
                project_link=None,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=1
            )
            id += 1
    '''
    Manual changes:
    * Estimation, simulation and control for optimal containment of COVID-19 ---- title and place has to be corrected
    * The joint corona hotline for Danish public authorities, Danish Red Cross: DKK 500,000 ---- insert description
    '''