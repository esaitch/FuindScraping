# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class CarlsbergfondetSpider(scrapy.Spider):
    name = 'carlsberg'
    pid = '05'
    start_id = 1
    allowed_domains = ['carlsbergfondet.dk']
    start_urls = ['https://www.carlsbergfondet.dk/da/Forskningsaktiviteter/Bevillingsstatistik/Bevillingsoversigt?year=2020&page=1',
                  'https://www.carlsbergfondet.dk/da/Forskningsaktiviteter/Bevillingsstatistik/Bevillingsoversigt?year=2021&page=1']

    covid_related_studies = ['ali salanti', 'michael bang petersen', 'lone simonsen', 'mette birkedal bruun', 'tina lupton']

    '''
    We scrape Carlsbergfondet's list of funded projects from here:
    https://www.carlsbergfondet.dk/da/Forskningsaktiviteter/Bevillingsstatistik/Bevillingsoversigt 
    
    We only look at the years 2020 and 2021 (in total, 306 projects).
    
    The following article lists 5 covid related projects that were funded:
    https://www.carlsbergfondet.dk/da/Nyheder/Nyt%20fra%20fondet/Nyheder/95%20mio%20kr%20til%20at%20accelerere%20indsatsen%20mod%20COVID19
    
    We match the names from this article, with the scraped projects from their website and mark the 5 projects as covid_specific.
    '''

    def parse(self, response):
        for project in response.xpath('//div[@class="comp__thumbnails--bevillinger"]/div/div'):
            name = project.xpath('.//h5/a/text()').extract_first() or project.xpath('.//h5/text()[1]').extract_first()
            # print('page: ' + response.url.split('page=')[-1], name.strip())

            detail_url = project.xpath('.//a/@href').extract_first()

            funditem = FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name.strip(),
                co_pi=None,
                pi_affiliation=project.xpath('.//p[contains(.,"Institution")]/following-sibling::p[1]/text()').extract_first(),
                gender=None,
                career_stage=project.xpath('.//p[contains(.,"Titel")]/following-sibling::p[1]/text()').extract_first(),
                country_of_origin=None,
                funder='Carlsbergfondet',
                grant_programme=project.xpath('.//p[contains(.,"Bevillingstype")]/following-sibling::p[1]/text()').extract_first().strip(),
                title=project.xpath('.//p[contains(.,"Projektnavn")]/following-sibling::p[1]/text()').extract_first(),
                summary=None,
                award_application_date=project.xpath('.//span[@class="title__date"]/text()').extract_first(),
                start_date=None,
                end_date=None,
                amount_awarded=re.findall(r'\d+', project.xpath('.//span[@class="title__amount"]/text()').extract_first().replace('.', ''))[0],
                research_area=None,
                project_link=response.urljoin(detail_url),
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=1 if name.strip().lower() in self.covid_related_studies else 0,
            )

            # increase id for next project
            self.start_id += 1

            # parse detail page with summary
            if detail_url:
                yield scrapy.Request(url=response.urljoin(detail_url), callback=self.parse_details, meta={'funditem': funditem})
            else:
                yield funditem

        # pagination
        next_page = response.xpath('//li[@id="phcontent_0_liPaginateRight"]/a/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        funditem = response.meta['funditem']

        funditem['summary'] = '\n'.join([line.strip() for line in response.xpath('//article[@class="article"]//text()').extract()]).strip()

        yield funditem
