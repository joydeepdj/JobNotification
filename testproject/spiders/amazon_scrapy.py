import scrapy
from ..items import TestprojectItem

class AmazonScrapy(scrapy.Spider):
    name = 'product'
    start_urls = [
        'https://www.sarkariresult.com/latestjob.php'
    ]

    def parse(self, response):
        items = TestprojectItem()
        jobs = response.css('#post')
        for ul in jobs:
            job_name = ul.css('li a::text').extract()
            job_link = ul.css('a::attr(href)').extract()
            #job_link = response.css()
            items['job_name'] = job_name
            items['job_link'] = job_link
            items['job_type']  = 'govt'
            yield items


