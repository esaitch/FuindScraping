# -*- coding: utf-8 -*-

import scrapy
import re
import json


class DNRFEmailSpider(scrapy.Spider):
    name = 'dnrf_email'
    start_urls = ['https://dg.dk/forskningsaktiviteter/centers-of-excellence/aktive-center-of-excellence/',
                  'https://dg.dk/forskningsaktiviteter/dnrf-chair/aktive-dnrf-chairs/']

    # parse dnrf data
    with open('../outputs/dnrf_output.json', encoding='utf-8') as js:
        dnrf_js = json.load(js)

    # get list of names
    names = [i['pi'].lower().strip() for i in dnrf_js]

    # create data set with header
    with open('dnrf_emails.csv', 'a') as data:
        data.write('funder' + ';' + 'pi' + '; ' + 'email' + '\n')

    def parse(self, response):
        for project in response.xpath('//div[@class="archive-grid"]/div'):
            p_url = project.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url=p_url, callback=self.parse_project)

    def parse_project(self, response):
        def get_info(want):
            return response.xpath('//div[@class="data"][contains(.,"%s")]/p[2]/text()' % want).extract_first()

        name_title = get_info('Centerleder') or get_info('DNRF Chair')
        name = re.split(r'Professor', name_title)[-1].strip()
        if name.lower().strip() not in self.names:
            return

        email = response.xpath('//div[@class="contact-person"]//a/@href').extract_first().split(':')[-1].strip()

        with open('dnrf_emails.csv', 'a') as data:
            data.write('dnrf' + ';' + name + '; ' + email + '\n')
