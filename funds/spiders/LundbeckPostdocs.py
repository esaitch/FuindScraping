# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class LundbeckPostdocsSpider(scrapy.Spider):
    name = 'lundbeckpostdocs'
    pid = '04'
    allowed_domains = ['lundbeckfonden.com']
    start_urls = ['https://lundbeckfonden.com/uddelinger-priser/har-vi-stoettet/lf-postdocs?year=All']

    handle_httpstatus_list = [403]

    custom_settings = {
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408]
    }

    '''
    Scraping only from year 2020 and 2021 from the projects portfolio:
    https://lundbeckfonden.com/uddelinger-priser/har-vi-stoettet/lf-postdocs?year=All 
    
    Matching these with the list of covid related studies here: 
    https://lundbeckfonden.com/nyheder/lundbeckfonden-uddeler-65-mio-kr-til-sundhedsvidenskabelige-forskere 
    
    The following names from the article above, cannot be found in the projects portfolio:
    Marija Nisavic    
    Narcis Adrian Petriman   
    Jan Heiner Driller
    '''

    def start_requests(self):
        # parse article of covid related projects
        yield scrapy.Request(
            url='https://lundbeckfonden.com/nyheder/lundbeckfonden-uddeler-65-mio-kr-til-sundhedsvidenskabelige-forskere',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
            callback=self.parse_covid_projects
        )

    def parse_covid_projects(self, response):
        summ = response.xpath('//div[@class="field field-content"]/p[position()>2]/text()').extract()
        names = [s.split(',')[0].strip().lower() for s in summ]

        # # correct spelling mistakes
        for i, name in enumerate(names):
            if name == 'katrine louise jensen':
                names[i] = 'kathrine louise jensen'
            elif name == 'nathalie beschorner':
                names[i] = 'natalie beschorner'

        # parse all projects
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
                callback=self.parse,
                meta={'covid_projects': names}
            )

    def parse(self, response):
        id = 1
        for project in response.xpath('//div[@class="view-content"]/div[contains(.,"2020") or contains(.,"2021")]//li'):
            project_url = project.xpath('.//a/@href').extract_first()

            title = project.xpath('.//div[@class="field node-title"]/div/a/text()').extract_first() or \
                    project.xpath('.//div[@class="field node-title"]/div/text()').extract_first()

            name = project.xpath('.//h1/text()').extract_first().strip()
            # check if this is a covid related project
            covid_related = 0
            if name.lower() in response.meta['covid_projects']:
                covid_related = 1

            funditem = FundItem(
                id=ScrapingTool.create_project_id(self.pid, id),
                pi=name,
                co_pi=None,
                pi_affiliation=project.xpath('.//div[@class="field field-applicant-institution"]/text()').extract_first().strip(),
                gender=None,
                career_stage=project.xpath('.//div[@class="field field-applicant-title"]/text()').extract_first().strip(),
                country_of_origin=None,
                funder='Lundbeckfonden',
                grant_programme=project.xpath('.//div[@class="field__item"]/text()').extract_first().strip(),
                title=title.strip(),
                summary=None,
                award_application_date=project.xpath('.//div[@class="field field-funding-year"]/text()').extract_first().strip(),
                start_date=None,
                end_date=None,
                amount_awarded=int(
                    re.findall(r'\d+', project.xpath('.//div[@class="field field-funding-amount-number field--label-inline"]/div/following-sibling::text()').extract_first().replace('.', ''))[0]),
                research_area=None,
                project_link=response.urljoin(project_url) if project_url else response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=covid_related
            )
            id += 1

            if project_url:
                yield scrapy.Request(url=response.urljoin(project_url), callback=self.parse_project_details,
                                     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
                                     meta={'funditem': funditem})

            else:
                yield funditem

    def parse_project_details(self, response):
        funditem = response.meta['funditem']

        funditem['summary'] = response.xpath('//div[@class="alpha"]//p//text()').extract_first().strip()
        funditem['grant_programme'] = response.xpath('//div[@class="field field-category field--label-inline"]/div/following-sibling::text()').extract_first().strip()

        yield funditem