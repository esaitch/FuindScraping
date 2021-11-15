# -*- coding: utf-8 -*-

import scrapy
import re
import json

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class VeluxVillumSpider(scrapy.Spider):
    name = 'veluxvillum'
    pid = '19'
    start_id = 1
    start_urls = ['https://veluxfoundations.dk/upload/db-en.json?r2m8j4']

    '''
    The projects can be found here: 
    https://veluxfoundations.dk/en/about/projects-granted#

    The API can be accessed here: 
    https://www.tryghed.dk/api/donations/mix?language=da&templateName=Donation&templateName=Partner%20Project%20Page&templateName=Trygfonden%20Project%20Page
    - the page size can be changed: &pageSize=30

    Only including projects from 2020 and 2021
    
    Output is then matched against the velux scraping output - if the title/name is the same, covid_specific is set to 1
    '''

    def parse(self, response):
        # load velux scraping output - covid studies only
        with open('veluxcovid_output.json', encoding='utf-8') as js:
            velux_covid = json.load(js)

        velux_covid_names = [p['pi'].lower().strip() for p in velux_covid]
        velux_covid_titles = [p['title'].lower().strip() for p in velux_covid]

        # load website data
        data = json.loads(response.body)

        for project in data['grants']:
            if int(project['date']['y']) < 2020:
                continue

            name = project['appl'] or None
            title = project['title'].strip()

            covid = 0
            if (name and name.lower().strip() in velux_covid_names) or title.lower().strip() in velux_covid_titles:
                covid = 1

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name,
                co_pi=None,
                pi_affiliation=project['dep'],
                gender=None,
                career_stage=project['appl_job'] or None,
                country_of_origin=None,
                funder=project['board'],
                grant_programme=project['area'],
                title=title,
                summary=None,
                award_application_date='-'.join(str(x) for x in project['date'].values()),
                start_date=None,
                end_date=None,
                amount_awarded=int(project['amount']),
                research_area=project['area'],
                project_link='https://veluxfoundations.dk/en/about/projects-granted#/',
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=covid,
            )

            self.start_id += 1
