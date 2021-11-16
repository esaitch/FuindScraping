# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class EnergistyrelsenSpider(scrapy.Spider):
    name = 'energistyrelsen'
    pid = '27'
    start_id = 1
    allowed_domains = ['eudp.dk']
    start_urls = ['https://eudp.dk/projekter?f%5B0%5D=program%3A79&f%5B1%5D=year%3A2020&f%5B2%5D=year%3A2021']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
                callback=self.parse
            )


    def parse(self, response):
        for project in response.xpath('//div[@class="view-content"]/div'):
            p_url = project.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url=response.urljoin(p_url),
                                 headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
                                 callback=self.parse_project)

        if next_page := response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').extract_first():
            yield scrapy.Request(url=response.urljoin(next_page),
                                 headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
                                 callback=self.parse)

    def parse_project(self, response):
        amount = response.xpath('//strong[contains(.,"Støttebeløb")]/following-sibling::text()[1]').extract_first()
        if 'mio' in amount:
            string_int = re.findall(r'\d+(?:\.\d+)?', amount.replace(',', '.'))[0]
            amount = int(float(string_int) * 1000000)

        period = response.xpath('//strong[contains(.,"Periode")]/following-sibling::text()[1]').extract_first()

        title = response.xpath('//div[@class="field field-original-title field--label-inline"]/div/following-sibling::text()').extract_first() or \
                response.xpath('//h2/text()').extract_first()

        place = (response.xpath('//div[@class="field field-company-ref"]/text()').extract_first() or '').strip()
        place2 = (response.xpath('//div[@class="field field-department"]/text()').extract_first() or '').strip()

        yield FundItem(
            id=ScrapingTool.create_project_id(self.pid, self.start_id),
            pi=None,
            co_pi=None,
            pi_affiliation=(place + ', ' + place2).strip().rstrip(',').lstrip(',').strip(),
            gender=None,
            career_stage=None,
            country_of_origin=None,
            funder='Energistyrelsen',
            grant_programme=response.xpath('//div[@class="field field-program-ref field--label-inline"]/div/following-sibling::text()').extract_first().strip(),
            title=title.strip(),
            summary='\n'.join(response.xpath('//div[@class="field field-content"][contains(.,"Projektbeskrivelse")]/p//text()').extract()),
            award_application_date=response.xpath('//strong[contains(.,"Bevillingsår")]/following-sibling::text()[1]').extract_first().strip(),
            start_date=re.findall(r'\d{4}', period)[0],
            end_date=re.findall(r'\d{4}', period)[1],
            amount_awarded=amount,
            research_area=None,
            project_link=response.url,
            funded=1,
            amount_sought=None,
            review_score=None,
            covid_specific=0,
        )

        self.start_id += 1
