import scrapy
from urllib.parse import urljoin

class SpidercrawlerSpider(scrapy.Spider):
    name = "spidercrawler"
    allowed_domains = ["hdtoday.tv"]
    start_urls = ["https://hdtoday.tv/movie"]
    page_limit = 500  

    def __init__(self, *args, **kwargs):
        super(SpidercrawlerSpider, self).__init__(*args, **kwargs)
        self.page_count = 0 

    def parse(self, response):
        movies = response.css('div.flw-item')
        for movie in movies:
            yield {
                'name': movie.css('h2 a::text').get(),
                'year': movie.css('div span::text').get(),
                'duration': movie.css('.fdi-duration::text').get(),
                'url': movie.css('h2 a').attrib['href'],
            }

        
        next_page = response.css('li.page-item a::attr(href)').get()

        if next_page is not None and self.page_count < self.page_limit:
            self.page_count += 1 
            next_page_url = urljoin(response.url, next_page)
            self.log(f'Next Page URL: {next_page_url}')

            
            yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)
        else:
            self.log('Crawling completed or page limit reached.')


import logging
logging.getLogger('scrapy').setLevel(logging.DEBUG)
