import scrapy

class GeneralSpider(scrapy.Spider):
    name = "general"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    allowed_domains = ['www.mewa.gov.sa']

    def start_requests(self):
        url = "https://www.mewa.gov.sa/ar/Pages/default.aspx"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # recursive access to website links
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