# -*- coding: utf-8 -*-

import scrapy
import re
import json

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class NovoNordiskAllSpider(scrapy.Spider):
    name = 'novoall'
    pid = '20'
    start_id = 1
    allowed_domains = ['novonordiskfonden.dk']
    start_urls = ['https://novonordiskfonden.dk/wp-admin/admin-ajax.php?language=da&action=fetch_bevillingslister_from_search&offset=0&yf=2020&yt=2021&f=year&s=desc']

    '''
    Scraping all projects from here:
    https://novonordiskfonden.dk/da/bevillingslister/?yf=2020&yt=2021 
    
    Match these projects agains novocovid output. If pi and amount_awarded matches, the covid_specific field is set to 1 and the grant_programme is updated
    
    Manual changes:
    "Temporary emergency shelters and soup kitchens" from Røde Kors is NOT covid_specific
    '''

    # parse novo covid data
    with open('novocovid_output.json', encoding='utf-8') as js:
        novo_covid = json.load(js)

    def parse(self, response):
        projects = response.xpath('//div[@class="nnf-grant-list__item row single-grant"]')

        for project in projects:
            # career stage is only listed sometimes
            info = project.xpath('./div[1]/div/text()').extract()
            name = info[0].strip()
            career = None
            if len(info) > 1:
                name = info[1].strip()
                career = info[0].strip()

            # if no place/affiliation is listed, the organisation is listed instead of a name. We can use the name as affiliation as well
            place = project.xpath('./div[2]/div[2]/text()').extract_first() or name

            funditem = FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name,
                co_pi=None,
                pi_affiliation=place.strip(),
                gender=None,
                career_stage=career,
                country_of_origin=None,
                funder='Novo Nordisk',
                grant_programme=None,
                title=None,
                summary=project.xpath('./div[3]/div[2]/text()').extract_first(),
                award_application_date=project.xpath('./div[5]/div[2]/text()').extract_first().strip(),
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'\d+', project.xpath('./div[4]/div[@class="nnf-grant-list__info-text"]/text()').extract_first().replace('.', ''))[0]),
                research_area='Biomedical and Natural Sciences',
                project_link=None,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0
            )
            self.start_id += 1

            # check if this project is in the novo covid crawling. if so, update covid_specific and grant_programme
            # check by pi and amount_awarded
            if matches := list(p for p in self.novo_covid if name.strip() in p['pi']):
                for m in matches:
                    if m['amount_awarded'] == funditem['amount_awarded']:
                        funditem['covid_specific'] = 1
                        funditem['grant_programme'] = m['grant_programme']

            yield funditem

        # if there are any projects on the requestet site, go to next 'page'
        # if the page was empty, stop the crawling
        if projects:
            current_offset = int(re.findall(r'offset=(\d+)', response.url)[0])
            next_url = 'https://novonordiskfonden.dk/wp-admin/admin-ajax.php?language=da&action=fetch_bevillingslister_from_search&offset=%s&yf=2020&yt=2021&f=year&s=desc' % \
                       str(int(current_offset) + 20)

            yield scrapy.Request(url=next_url, callback=self.parse)
