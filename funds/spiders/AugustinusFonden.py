# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class AugustinusFondenSpider(scrapy.Spider):
    name = 'augustinusfonden'
    pid = '13'
    start_id = 1
    start_urls = ['https://docs.google.com/spreadsheets/d/e/2PACX-1vSHMY7_vxY_Tf7ybhTvgYOJ-gu1Q9CLAJ4rxBR9DRWEXCkXVxzyZGr9djwKIjazC_RD29cGX07OyPIn/pubhtml#']

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    '''
    The projects can be found in a pdf here: 
    https://augustinusfonden.dk/wp-content/uploads/2021/03/samlede-bevillinger-2020.pdf

    I have exported the pdf to Google Sheets, which is easier to extract data from/scrape
    https://docs.google.com/spreadsheets/d/1if_mApM8sdStjselenhOHMaXQNN9p_7KyO2P4muI5dg/edit?usp=sharing
    '''

    def parse(self, response):
        categories = response.xpath('//ul[@id="sheet-menu"]/li/a/text()').extract()

        for index, sheet in enumerate(response.xpath('//div[@id="sheets-viewport"]/div')):
            category = categories[index]

            for project in sheet.xpath('.//tbody/tr'):
                yield FundItem(
                    id=ScrapingTool.create_project_id(self.pid, self.start_id),
                    pi=project.xpath('./td[1]//text()').extract_first().strip(),
                    co_pi=None,
                    pi_affiliation=project.xpath('./td[1]//text()').extract_first().strip(),
                    gender=None,
                    career_stage=None,
                    country_of_origin=None,
                    funder='Augustinus Fonden',
                    grant_programme=None,
                    title=None,
                    summary=project.xpath('./td[2]//text()').extract_first().strip(),
                    award_application_date='2020',
                    start_date=None,
                    end_date=None,
                    amount_awarded=int(project.xpath('./td[3]//text()').extract_first().strip()),
                    research_area=category,
                    project_link='https://augustinusfonden.dk/wp-content/uploads/2021/03/samlede-bevillinger-2020.pdf',
                    funded=1,
                    amount_sought=None,
                    review_score=None,
                    covid_specific=0,
                )

                self.start_id += 1
