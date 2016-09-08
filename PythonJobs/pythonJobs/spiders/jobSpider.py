# -*- coding: utf-8 -*-
import scrapy
import chardet
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pythonJobs.items import PythonjobsItem
from scrapy.contrib.loader import ItemLoader

class JobspiderSpider(CrawlSpider):
    name = 'jobSpider'
    allowed_domains = ['search.51job.com','jobs.51job.com']
    start_urls = ['http://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html']

    rules = (
        Rule(LinkExtractor(allow=r'jobs.52job.com'), callback='parse_item'),
        Rule(LinkExtractor(  ))
    )


    def parse_item(self, response):
        # text = response.body
        # content_type = chardet.detect(text)
        # if content_type['encoding'].lower() != 'utf-8':
        #     text = text.decode(content_type['encoding'])
        # text = text.encode('utf-8')
        # response = response.replace(body=text)
        i = ItemLoader(item=PythonjobsItem(),response=response)
        i.add_xpath('title','//div[@class="in"]/div[@class="cn"]/h1/@title')
        i.add_value('url',response.url)
        i.add_xpath('city','//div[@class="in"]/div[@class="cn"]/span[@class="lname"]/text()')
        i.add_xpath('company','//div[@class="in"]/div[@class="cn"]/p[@class="cname"]/a/text()')
        i.add_xpath('location','')
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
