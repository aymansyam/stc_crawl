import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from time import sleep

JAVASCRIPT_LOAD_TIME = 5

# all pages use JavaScript and need selenium to load.
# [TODO] use other framework besides selenium to increase performance.
def selenium_get(driver, response):
    driver.get(response.url)

    # Add a delay for JavaScript to load
    sleep(JAVASCRIPT_LOAD_TIME)

    html = driver.page_source
    resp = Selector(text=html)
    return resp

class ProductsSpider(scrapy.Spider):
    name = "products"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'FEEDS': { 'data.json': { 'format': 'json'}}
    }

    allowed_domains = ["www.stc.com.sa"]
    

    def start_requests(self):
        url = "https://www.stc.com.sa/content/stc-public-store/sa/ar/public-store-landing-page.html"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # public store landing page and categories
        resp = selenium_get(webdriver.Chrome(), response)

        elements = resp.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cmp-ShopCards__button contentWrapperCategory RTL", " " ))]/ul/li')
        for element in elements:
            link = element.xpath('./a/@href').get()
            if link is not None:
                yield response.follow(link, self.parse_link, cb_kwargs=dict(driver=webdriver.Chrome()))

    
    def parse_link(self, response, driver):
        # product list
        resp = selenium_get(driver, response)

        elements = resp.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "card-link", " " ))]/@href').getall()
        yield from response.follow_all(elements, self.parse_product, cb_kwargs=dict(driver=driver))

    def parse_product(self, response, driver):
        # product description
        resp = selenium_get(driver, response)

        title = resp.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cmp-product-name", " " ))]/text()').get()
        yield {
            'title': title
        }



        


