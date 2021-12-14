import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%B4%D0%B5%D1%82%D0%B5%D0%BA%D1%82%D0%B8%D0%B2%D1%8B/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@title="Следующая"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class="cover"]/@href').getall()
        for i in links:
            yield response.follow(i, callback=self.book_pars)

    def book_pars(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        author = response.xpath('//a[@data-event-label="author"]/text()').get()
        price = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        price_new = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        rate = response.xpath('//div[@id="rate"]/text()').get()
        url = response.url
        yield BooksparserItem(name=name, author=author, price=price, price_new=price_new, rate=rate, url=url)

