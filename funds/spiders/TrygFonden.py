# -*- coding: utf-8 -*-

import scrapy
import re
import json

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class TrygFondenSpider(scrapy.Spider):
    name = 'tryg'
    pid = '18'
    start_id = 1
    start_urls = ['https://www.tryghed.dk/api/donations/mix?language=da&templateName=Donation&templateName=Partner%20Project%20Page&templateName=Trygfonden%20Project%20Page&pageSize=6000']

    '''
    The projects can be found here: 
    https://www.tryghed.dk/saadan-stoetter-vi/projekter-og-donationer
    
    The API can be accessed here: 
    https://www.tryghed.dk/api/donations/mix?language=da&templateName=Donation&templateName=Partner%20Project%20Page&templateName=Trygfonden%20Project%20Page
    - the page size can be changed: &pageSize=30
    
    Only including projects from 2020 and 2021
    '''

    def parse(self, response):
        data = json.loads(response.body)

        for project in data['Hits']:
            #only include 2020 and 2021 projects
            if 'PublishedYear' in project and (year := project['PublishedYear']) < 2020:
                continue

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=None,
                co_pi=None,
                pi_affiliation=project['Institution'],
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder='Tryg Fonden',
                grant_programme=project['TemplateName'] + ', ' + project['FocusArea'],
                title=project['Title'],
                summary=project['Description'],
                award_application_date=year,
                start_date=None,
                end_date=None,
                amount_awarded=int(project['Amount']) if project['Amount'] else None,
                research_area=project['TargetArea'],
                project_link='https://www.tryghed.dk/' + project['Url'],
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0,
            )

            self.start_id += 1
