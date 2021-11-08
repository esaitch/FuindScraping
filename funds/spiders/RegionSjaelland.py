# -*- coding: utf-8 -*-

import scrapy
import re
import pdfplumber

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class RegionSjaellandSpider(scrapy.Spider):
    name = 'regionsjaelland'
    pid = '10'
    start_id = 1
    start_urls = ['https://docs.google.com/spreadsheets/d/e/2PACX-1vSsl0V0WOZFC7gY4g1t8XKrSWzOvhhPG-rXcNLq-XrwEyIh9Gi12tCGIARWJiNdVx1uDo7ZhqgPpz4y/pubhtml']

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    '''
    The projects can be found in a pdf on this site: 
    https://www.regionsjaelland.dk/Sundhed/forskning/forfagfolk/forskningsfinansiering/Sider/oekonomi.aspx
    
    I have exported the pdf to Google Sheets, which is easier to extract data from/scrape
    https://docs.google.com/spreadsheets/d/1BHSnYQpak2pmLfiHsuEzbDt1wmVvrTEEsuWJfMpVoPE/edit?usp=sharing 
    '''

    def parse(self, response):
        for project in response.xpath('//tbody/tr[position()>1]'):
            first_name = project.xpath('./td[1]//text()').extract_first()
            last_name = project.xpath('./td[2]//text()').extract_first()

            location = project.xpath('./td[5]//text()').extract_first().strip()
            department = project.xpath('./td[4]//text()').extract_first().strip()

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=first_name.strip() + ' ' + last_name.strip(),
                co_pi=None,
                pi_affiliation=location + ', ' + department,
                gender=None,
                career_stage=''.join(project.xpath('./td[3]//text()').extract()).strip(),
                country_of_origin=None,
                funder='Region Sjælland',
                grant_programme=None,
                title=''.join(project.xpath('./td[6]//text()').extract()).strip(),
                summary=None,
                award_application_date=None,
                start_date=None,
                end_date=None,
                amount_awarded=int(project.xpath('./td[7]//text()').extract_first().strip()),
                research_area=None,
                project_link='https://www.regionsjaelland.dk/Sundhed/forskning/forfagfolk/forskningsfinansiering/Sider/oekonomi.aspx',
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0,
            )

            self.start_id += 1