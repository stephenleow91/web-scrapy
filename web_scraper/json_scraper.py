import re
import json
import scrapy


class JsonCrawler(scrapy.Spider):
    name = "json_spider"
    start_urls = ['http://quotes.toscrape.com/js/']

    def parse(self, response):
        data = re.findall("var data =(.+?);\n",
                          response.body.decode("utf-8"), re.S)
        ls = []

        if data:
            ls = json.loads(data[0])

        if ls:
            print(ls)
