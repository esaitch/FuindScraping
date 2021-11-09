# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class DNRFSpider(scrapy.Spider):
    name = 'dnrf'
    pid = '14'
    start_id = 1
    start_urls = ['https://dg.dk/forskningsaktiviteter/centers-of-excellence/aktive-center-of-excellence/',
                  'https://dg.dk/forskningsaktiviteter/dnrf-chair/aktive-dnrf-chairs/']

    '''
    Two types of programmes:
    https://dg.dk/forskningsaktiviteter/centers-of-excellence/aktive-center-of-excellence/ 
    https://dg.dk/forskningsaktiviteter/dnrf-chair/aktive-dnrf-chairs/ 
    
    There is a third, but the page is empty:
    https://dg.dk/pionercentre/aktive-pionercentre/
    
    Scraping all active projects, even when funding was granted before 2020, since they are still ongoing
    
    None is marked at covid related
    '''

    def parse(self, response):
        programme = response.xpath('//h1/text()').extract_first().replace('Aktive', '').strip()

        for project in response.xpath('//div[@class="archive-grid"]/div'):
            p_url = project.xpath('.//a/@href').extract_first()

            yield scrapy.Request(url=p_url, callback=self.parse_project, meta={'programme': programme})

    def parse_project(self, response):
        def get_info(want):
            return response.xpath('//div[@class="data"][contains(.,"%s")]/p[2]/text()' % want).extract_first()

        period = get_info('Periode')
        granted = get_info('Bevilling')
        if not period:
            # there is a mistake on the website where period field sometimes is switched with grant sum, and the grant sum then is not listed
            period = granted
            granted = None

        start = period.split('-')[0].strip()
        end = period.split('-')[1].strip()

        if granted:
            if 'mio' in granted:
                string_int = re.findall(r'\d+(?:\.\d+)?', granted.replace(',', '.'))[0]
                granted = int(float(string_int) * 1000000)


        name_title = get_info('Centerleder') or get_info('DNRF Chair')
        name = re.split(r'Professor', name_title)[-1].strip()
        career = name_title.replace(name, '').strip()

        info_link = response.xpath('//div[@class="data link"]//a/@href').extract_first()

        yield FundItem(
            id=ScrapingTool.create_project_id(self.pid, self.start_id),
            pi=name,
            co_pi=None,
            pi_affiliation=get_info('Værtsinstitution').strip(),
            gender=None,
            career_stage=career,
            country_of_origin=None,
            funder='Danish National Research Foundation',
            grant_programme=response.meta['programme'],
            title=response.xpath('//h1/text()').extract_first(),
            summary='\n\n'.join(response.xpath('//article[@class="item item-text"]/p/text()').extract()).strip(),
            award_application_date=re.findall(r'\d{4}', start)[0],
            start_date=start,
            end_date=end or None,
            amount_awarded=granted,
            research_area=None,
            project_link=[response.url, info_link] if info_link else response.url,
            funded=1,
            amount_sought=None,
            review_score=None,
            covid_specific=0,
        )

        # increase id for next project
        self.start_id += 1
