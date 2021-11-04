# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class LundbeckAllSpider(scrapy.Spider):
    name = 'lundbeckall'
    pid = '06'
    start_id = 1
    allowed_domains = ['lundbeckfonden.com']
    start_urls = ['https://lundbeckfonden.com/uddelinger-priser/har-vi-stoettet/alle-bevillinger?year=All&c=All']

    handle_httpstatus_list = [403]

    custom_settings = {
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408],
        'DOWNLOAD_DELAY': 0.5,
    }

    '''
    Scraping only from year 2020 and 2021 from here:
    https://lundbeckfonden.com/uddelinger-priser/har-vi-stoettet/alle-bevillinger?year=All&c=All
    
    Using the 'Corona' category and additionally matching with the list of covid related studies here: 
    https://lundbeckfonden.com/nyheder/lundbeckfonden-uddeler-65-mio-kr-til-sundhedsvidenskabelige-forskere 
    
    The following names from the article above, cannot be found in the portfolio:
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
                callback=self.parse_all,
                meta={'covid_projects': names}
            )

    def parse_all(self, response):
        covid_projects = response.meta['covid_projects']

        for project in response.xpath('//table/tbody/tr'):
            # only scrape 2020 and 2021 projects
            year = project.xpath('./td[1]/text()').extract_first().strip()
            include = ['2020', '2021']
            if year not in include:
                continue

            # Sometimes amount awared is not listed. Skip these
            if not (amount := project.xpath('./td[5]/text()').extract_first().strip()):
                continue

            # sometimes both affiliation and career title is listed. sometimes only affiliation
            p_info = project.xpath('./td[3]/div/text()').extract()
            name = p_info[0].strip()

            career = None
            affiliation = None
            if len(p_info) > 2:
                career = p_info[1].strip()
                affiliation = p_info[2].strip()
            elif len(p_info) > 1:
                affiliation = p_info[1].strip()

            category = project.xpath('./td[2]/text()').extract_first().strip()

            # check if this is a covid related project
            # use the 'Kategori' on the site and also match against the article
            covid_related = 1 if 'corona' in category.lower() else 0
            if name.lower() in covid_projects:
                covid_related = 1

            project_url = project.xpath('./td[4]/a/@href').extract_first()

            funditem = FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name,
                co_pi=None,
                pi_affiliation=affiliation,
                gender=None,
                career_stage=career,
                country_of_origin=None,
                funder='Lundbeckfonden',
                grant_programme=category,
                title=project.xpath('./td[4]//text()').extract_first().strip(),
                summary=None,
                award_application_date=year,
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'\d+', amount.replace('.', ''))[0]),
                research_area=None,
                project_link=response.urljoin(project_url) if project_url else response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=covid_related
            )
            self.start_id += 1

            # yield project detail page if it exists
            if project_url:
                yield scrapy.Request(url=response.urljoin(project_url),
                                     callback=self.parse_project_details,
                                     meta={'funditem': funditem},
                                     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'})
            else:
                yield funditem

        # check if last project on page is from an included year. If so, also check next page. If not, terminate
        if response.xpath('//table/tbody/tr[position()=last()]/td[1]/text()').extract_first().strip() in include:
            next_page = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').extract_first()
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_all, meta={'covid_projects': covid_projects},
                                 headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'})


    def parse_project_details(self, response):
        funditem = response.meta['funditem']

        funditem['summary'] = response.xpath('//div[@class="alpha"]//p//text()').extract_first().strip()
        funditem['grant_programme'] = response.xpath('//div[@class="field field-category field--label-inline"]/div/following-sibling::text()').extract_first().strip()

        yield funditem