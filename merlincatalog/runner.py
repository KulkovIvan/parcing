from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from merlincatalog.spiders.leroymerlinru import LeroymerlinruSpider
from merlincatalog import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    my_query = input('Enter your query')
    process.crawl(LeroymerlinruSpider, query='герметик')
    process.start()
