from pathlib import Path

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "neudesic"

    def start_requests(self):
        urls = [
            'https://employees.neudesic.com/apps',
            'https://employees.neudesic.com/faqs',
            'https://employees.neudesic.com/benefits/',
            'https://employees.neudesic.com/policies/',
            'https://employees.neudesic.com/team/',
            'https://employees.neudesic.com/values/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'neudesic-{page}.html'
        Path("./neudesic/" + filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')