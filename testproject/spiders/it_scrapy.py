import scrapy
from ..items import TestprojectItem

class AmazonScrapy(scrapy.Spider):
    name = 'it'
    start_urls = [
        'https://fresheropenings.com/off-campus-drive/',
        'https://fresherscamp.com/category/off-campus-jobs/'
    ]

    def parse(self, response):
        items = TestprojectItem()
        jobs = response.css('.td-module-title')
        #print(jobs[0])

        for ul in jobs:
            job_name = ul.css('a::text').extract()
            job_link = ul.css('a::attr(href)').extract()
            #job_link = response.css()
            items['job_name'] = job_name
            items['job_link'] = job_link
            items['job_type'] ='it'
            yield items


