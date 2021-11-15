# -*- coding: utf-8 -*-

import scrapy
import re

from funds.items.fundItem import FundItem
from funds.tools.scrapingTool import ScrapingTool


class DanishCancerSocietySpider(scrapy.Spider):
    name = 'cancersociety'
    pid = '21'
    start_id = 1
    allowed_domains = ['cancer.dk']

    '''
    scraping from here: 
    https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/ 
    
    EXCEPT these that are manually added in cancersociety_manual_output:
    Manually add the 2 relevant for 2020/2021 from: https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/professorater-p2/ (Tarec El-Galaly and Niels Christian Hvidt)
    Manually add 2020/2021 projects from: https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/juniorforskerpriser/ 
    '''

    def start_requests(self):
        individual_p = ['https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/kraeftens-bekaempelses-videnskabelige-udvalg-biologi-klinik-kbvu-bk-tidligere-kbvu/kbvu-oversigt-over-projektbevillinger-givet-i-2020/',
                        'https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/kraeftens-bekaempelses-videnskabelige-udvalg-faellesudvalg-kbvu-bk-ms-skolarstipendier-udlandsophold-over-1-maaned-uden-loen/skolarstipendium/',
                        'https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/kraeftens-bekaempelses-videnskabelige-udvalg-faellesudvalg-kbvu-bk-ms-skolarstipendier-udlandsophold-over-1-maaned-uden-loen/udlandsophold-uden-loen-2021/']

        for url in individual_p:
            yield scrapy.Request(url=url, callback=self.parse_p)

        single_p = ['https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/kraeftens-bekaempelses-videnskabelige-udvalg-biologi-klinik-kbvu-bk-tidligere-kbvu/kbvu-bk-oversigt-over-projektbevillinger-givet-i-2021/',
                    'https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/kraeftens-bekaempelses-videnskabelige-udvalg-menneske-samfund-kbvu-ms-tidligere-kbpf-og-kpsk/kbvu-ms-projektbevillinger-givet-i-2021/']

        for url in single_p:
            yield scrapy.Request(url=url, callback=self.parse_single_p)

        no_bold = ['https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/kraeftens-bekaempelses-videnskabelige-udvalg-menneske-samfund-kbvu-ms-tidligere-kbpf-og-kpsk/kbpf-hoveduddeling-2020/']
        for url in no_bold:
            yield scrapy.Request(url=url, callback=self.parse_no_bold)

        multiple = ['https://www.cancer.dk/forskning/stoette-til-forskning/stoettet-forskning/knaek-cancer-midler/']
        for url in multiple:
            yield scrapy.Request(url=url, callback=self.parse_multiple)

    def parse_p(self, response):
        grant = response.xpath('//div[@class="contentbox"]/p/strong/text()').extract_first()
        grant = grant.split(' har')[0].strip()

        for project in response.xpath('//div[@class="contentbox dictionary-ready"]/p'):
            name = project.xpath('./strong/text()').extract_first()
            if not name:
                continue

            info = project.xpath('./text()[4]').extract_first()
            start = None
            end = None
            if '-' in info:
                start = re.findall(r'\d{4}', info)[0]
                end = re.findall(r'\d{4}', info)[1]

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name.strip(),
                co_pi=None,
                pi_affiliation=project.xpath('./text()[3]').extract_first().strip(),
                gender=None,
                career_stage=project.xpath('./text()[2]').extract_first().strip(),
                country_of_origin=None,
                funder='Danish Cancer Society',
                grant_programme=grant,
                title=project.xpath('./text()[1]').extract_first().strip(),
                summary=None,
                award_application_date=re.findall(r'\d{4}', response.xpath('//h1/text()').extract_first())[0],
                start_date=start,
                end_date=end,
                amount_awarded=int(re.findall(r'(\d+) kr', info.replace('.', ''))[0]),
                research_area='Medical Sciences',
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0
            )

            self.start_id += 1

    def parse_single_p(self, response):
        grant = response.xpath('//div[@class="contentbox"]/p/strong/text()').extract_first()
        grant = grant.split(' har')[0].strip()

        for project in response.xpath('//div[@class="contentbox dictionary-ready"]/p/strong'):
            info = project.xpath('./following-sibling::text()[2]').extract_first()
            start = None
            end = None
            if '-' in info:
                start = re.findall(r'\d{4}', info)[0]
                end = re.findall(r'\d{4}', info)[1]

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=project.xpath('./text()').extract_first(),
                co_pi=None,
                pi_affiliation=project.xpath('./following-sibling::text()[1]').extract_first().strip(),
                gender=None,
                career_stage=project.xpath('./preceding-sibling::text()[1]').extract_first().strip(),
                country_of_origin=None,
                funder='Danish Cancer Society',
                grant_programme=grant,
                title=project.xpath('./preceding-sibling::text()[2]').extract_first().strip(),
                summary=None,
                award_application_date=re.findall(r'\d{4}', response.xpath('//h1/text()').extract_first())[0],
                start_date=start,
                end_date=end,
                amount_awarded=int(re.findall(r'(\d+) kr', info.replace('.', ''))[0]),
                research_area='Medical Sciences',
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0
            )

            self.start_id += 1

    def parse_no_bold(self, response):
        grant = response.xpath('//div[@class="contentbox"]/p/strong/text()').extract_first()
        grant = grant.split(' har')[0].strip()

        for project in response.xpath('//div[@class="contentbox dictionary-ready"]/p'):
            name_career = project.xpath('./text()[2]').extract_first().strip()
            name = ' '.join(re.findall(r' ([A-Z][a-z]+)+', name_career))
            career = name_career.replace(name, '').strip()

            yield FundItem(
                id=ScrapingTool.create_project_id(self.pid, self.start_id),
                pi=name,
                co_pi=None,
                pi_affiliation=project.xpath('./text()[3]').extract_first().strip(),
                gender=None,
                career_stage=career,
                country_of_origin=None,
                funder='Danish Cancer Society',
                grant_programme=grant,
                title=project.xpath('./text()[1]').extract_first().strip(),
                summary=None,
                award_application_date=re.findall(r'\d{4}', response.xpath('//h1/text()').extract_first())[0],
                start_date=None,
                end_date=None,
                amount_awarded=int(re.findall(r'(\d+) kr', project.xpath('./text()[4]').extract_first().replace('.', ''))[0]),
                research_area='Medical Sciences',
                project_link=response.url,
                funded=1,
                amount_sought=None,
                review_score=None,
                covid_specific=0
            )

            self.start_id += 1

    def parse_multiple(self, response):
        grant = response.xpath('//h1/text()').extract_first().strip()

        for project in response.xpath('//div[@class="contentbox dictionary-ready"]/p/a'):
            title = project.xpath('./text()').extract_first()
            year = re.findall(r'\d{4}', title)[0]
            if '202' not in year:
                continue

            detail_url = project.xpath('./@href').extract_first()
            yield scrapy.Request(url=response.urljoin(detail_url), callback=self.parse_details, meta={'grant': grant, 'year': year})

    def parse_details(self, response):
        for project in response.xpath('//div[@class="contentbox dictionary-ready"]/p'):
            length = len([p for p in project.xpath('./text()').extract() if p and p.strip()])

            # if single project
            if length == 4:
                name_career = project.xpath('./text()[2]').extract_first().strip()
                name = ' '.join(re.findall(r' ([A-Z][a-z]+)+', name_career))
                career = name_career.replace(name, '').strip()

                info = project.xpath('./text()[4]').extract_first()
                start = None
                end = None
                if '-' in info:
                    start = re.findall(r'\d{4}', info)[0]
                    end = re.findall(r'\d{4}', info)[1]

                yield FundItem(
                    id=ScrapingTool.create_project_id(self.pid, self.start_id),
                    pi=name,
                    co_pi=None,
                    pi_affiliation=project.xpath('./text()[3]').extract_first().strip(),
                    gender=None,
                    career_stage=career,
                    country_of_origin=None,
                    funder='Danish Cancer Society',
                    grant_programme=response.meta['grant'],
                    title=project.xpath('./text()[1]').extract_first().strip(),
                    summary=None,
                    award_application_date=response.meta['year'],
                    start_date=start,
                    end_date=end,
                    amount_awarded=int(re.findall(r'(\d+) kr', info.replace('.', ''))[0]),
                    research_area='Medical Sciences',
                    project_link=response.url,
                    funded=1,
                    amount_sought=None,
                    review_score=None,
                    covid_specific=0
                )

                self.start_id += 1

            else:
                multiple = [p for p in project.xpath('./text()').extract() if p and p.strip()]
                split = [multiple[x:x+4] for x in range(0, len(multiple), 4)]
                for s in split:
                    name_career = s[1].strip()
                    name = ' '.join(re.findall(r' ([A-Z][a-z]+)+', name_career))
                    career = name_career.replace(name, '').strip()

                    info = s[3]
                    start = None
                    end = None
                    if '-' in info:
                        start = re.findall(r'\d{4}', info)[0]
                        end = re.findall(r'\d{4}', info)[1]

                    yield FundItem(
                        id=ScrapingTool.create_project_id(self.pid, self.start_id),
                        pi=name,
                        co_pi=None,
                        pi_affiliation=s[2].strip(),
                        gender=None,
                        career_stage=career,
                        country_of_origin=None,
                        funder='Danish Cancer Society',
                        grant_programme=response.meta['grant'],
                        title=s[0].strip(),
                        summary=None,
                        award_application_date=response.meta['year'],
                        start_date=start,
                        end_date=end,
                        amount_awarded=int(re.findall(r'(\d+) kr', info.replace('.', ''))[0]),
                        research_area='Medical Sciences',
                        project_link=response.url,
                        funded=1,
                        amount_sought=None,
                        review_score=None,
                        covid_specific=0
                    )

                    self.start_id += 1



