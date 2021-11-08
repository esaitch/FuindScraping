# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class NordeaSpider(scrapy.Spider):
    name = 'nordea'
    pid = '09'
    start_id = 1
    allowed_domains = ['nordeafonden.dk']

    def start_requests(self):
        # parse article of covid related projects
        yield scrapy.Request(
            url='https://nordeafonden.dk/det-stoetter-vi/det-har-vi-stoettet',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
            callback=self.parse
        )

    def parse(self, response):
        for project in response.xpath('//div[@class="item-list"]/ul/li'):
            p_url = project.xpath('.//div[@class="field node-title"]//a/@href').extract_first()
            category = project.xpath('.//li[@class="field__item"]/a/text()').extract_first()

            yield scrapy.Request(
                url=response.urljoin(p_url),
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
                callback=self.parse_project,
                meta={'category': category}
            )


    def parse_project(self, response):
        period = response.xpath('//div[@class="field field-project-period field--label-inline"]/div/following-sibling::text()').extract_first()
        if not period:
            return
        start = re.split(r'–|-', period)[0].strip()
        end = re.split(r'–|-', period)[1].strip()

        # only include project from 2020 and 2021
        # either starting in, or ending in or spanning over (i.e. 2019-2024)
        if '202' not in start and '202' not in end:
            return

        summ = response.xpath('//div[@class="field field-content"]/p/text()').extract()
        summ = '\n'.join([line.strip() for line in summ if line.strip() and len(line.strip()) > 5])

        amount = response.xpath('//div[@class="field field-funded-by field--label-inline"]/p/text()').extract_first()
        if 'mio' in amount:
            string_int = re.findall(r'\d+(?:\.\d+)?', amount.replace(',', '.'))[0]
            amount = int(float(string_int) * 1000000)
        else:
            amount = int(re.findall(r'\d+', amount.replace('.', ''))[0])

        name = response.xpath('//div[@class="field field-contact-person-name"]/text()').extract_first()
        if not name:
            return

        career_title = response.xpath('//div[@class="field"]/div[@class="field field-position"]/text()').extract_first()
        if not career_title:
            career_title = name.split(',')[-1].strip()
            name = name.split(',')[0].strip()

        yield FundItem(
            id=ScrapingTool.create_project_id(self.pid, self.start_id),
            pi=name.strip(),
            co_pi=None,
            pi_affiliation=response.xpath('//div[@class="field field-project-owner field--label-inline"]/p/text()').extract_first(),
            gender=None,
            career_stage=career_title.strip(),
            country_of_origin=None,
            funder='Nordea-fonden',
            grant_programme=None,
            title=response.xpath('//div[@class="field field-project-name field--label-inline"]/div/following-sibling::text()').extract_first().strip(),
            summary=summ,
            award_application_date=start,
            start_date=start,
            end_date=end,
            amount_awarded=amount,
            research_area=response.meta['category'],
            project_link=response.url,
            funded=1,
            amount_sought=None,
            review_score=None,
            covid_specific=0,
        )

        # increase id for next project
        self.start_id += 1
