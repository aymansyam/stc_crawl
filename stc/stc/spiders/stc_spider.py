import scrapy


class StcSpiderSpider(scrapy.Spider):
    name = "stc_spider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }
    # allowed_domains = ["www.stc.com.sa"]

    def start_requests(self):
        url = "https://www.stc.com.sa/content/stc-public-store/sa/ar/public-store-landing-page.html"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        elements = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cmp-ShopCards__button-list", " " ))]')
        for element in elements:
            link = element.xpath('./a/@href').get()
            if link is not None:
                yield response.follow(link, self.parse_link)


