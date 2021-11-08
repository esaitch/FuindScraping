# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class HelsefondenSpider(scrapy.Spider):
    name = 'helsefonden'
    pid = '07'
    start_id = 1
    allowed_domains = ['helsefonden.dk']

    def start_requests(self):
        yield scrapy.Request(
            url='https://helsefonden.dk/har-vi-stoettet?field_category_target_id%5B12%5D=12&combine=&t=43',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
            callback=self.parse_covid_projects
        )

    def parse_covid_projects(self, response):
        covid_projects = []
        for project in response.xpath('//div[@class="item-list"]//li'):
            name = project.xpath('.//div[@class="field field-project-manager field--label-inline"]/div/following-sibling::text()').extract_first().strip()
            covid_projects.append(name.lower())

        print(covid_projects)

        # now parse all projects
        yield scrapy.Request(
            url='https://helsefonden.dk/har-vi-stoettet?field_category_target_id%5B12%5D=12&combine=&t=All',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
            callback=self.parse, meta={'covid_projects': covid_projects}
        )

    def parse(self, response):
        covid_projects = response.meta['covid_projects']

        for project in response.xpath('//div[@class="item-list"]/ul/li'):
            name = project.xpath('.//div[@class="field field-project-manager field--label-inline"]/div/following-sibling::text()').extract_first() or ''
            affil = project.xpath('.//div[@class="field field-institution field--label-inline"]/div/following-sibling::text()').extract_first()

            amount = project.xpath('.//div[@class="field field-license field--label-inline"]/div/following-sibling::text()').extract_first().strip()

            year = project.xpath('.//div[@class="field field-license-year field--label-inline"]/div/following-sibling::text()').extract_first()

            funditem = FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name.strip() if name else None,
                co_pi=None,
                pi_affiliation=affil.strip() if affil else None,
                gender=None,
                career_stage=None,
                country_of_origin=None,
                funder='Helsefonden',
                grant_programme=None,
                title=project.xpath('.//h2/text()').extract_first().strip(),
                summary=''.join(project.xpath('.//div[@class="field field-content"]/p/text()').extract()).strip(),
                award_application_date=year.strip() if year else None,
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'\d+', amount.replace('.', ''))[0]),
                research_area=None,
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=1 if name.strip().lower() in covid_projects else 0
            )
            self.start_id += 1

            yield funditem

        # check if there is next page
        # also check if the last project on current page is from 2020. If not, there is no need to parse the next page
        last_project = response.xpath('//div[@class="field field-license-year field--label-inline"]/div/following-sibling::text()').extract()[-1]
        if '2020' in last_project or '2021' in last_project or len(last_project.strip()) > 4:
            next_page = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').extract_first()
            if next_page:
                yield scrapy.Request(
                    url=response.urljoin(next_page),
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'},
                    callback=self.parse, meta={'covid_projects': covid_projects}
                )
