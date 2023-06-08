import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from time import sleep

JAVASCRIPT_LOAD_TIME = 5

class GeneralSpider(scrapy.Spider):
    name = "general"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # all pages use JavaScript and need selenium to load.
    # [TODO] use other framework besides selenium to increase performance.
    def selenium_get(self, response):
        self.driver.get(response.url)

        # Add a delay for JavaScript to load (change depending on machine performance)
        # If you are getting null items, increase the sleep duration
        sleep(JAVASCRIPT_LOAD_TIME)

        html = self.driver.page_source
        resp = Selector(text=html)
        return resp
    
    # def __init__(self):
        # self.driver = webdriver.Chrome()

    def start_requests(self):
        url = "https://www.mewa.gov.sa/ar/Pages/default.aspx"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # public store landing page and categories
        # resp = self.selenium_get(response)
        href_elements = response.css('a::attr(href)')
        for href in href_elements:
            try:
                yield response.follow(href, self.parse)
            except:
                print('cannot follow link')

        # Save page content to an HTML file
        page = response.url.split("/")[-2]
        filename = 'mewa_dump/%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)