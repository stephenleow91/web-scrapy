import scrapy
import csv
import logging
import os


class AmazonScraper(scrapy.Spider):
    name = 'amazon_scraper'
    start_urls = ['https://www.amazon.com/s?k=java']
    directory = 'amazon/'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    def parse(self, response):
        INNER_SELECTOR = '//div[@class="a-section a-spacing-medium"]'

        for books in response.xpath(INNER_SELECTOR):
            information = self.get_information(books)
            self.write_to_file(information, response)

            NEXT_PAGE_SELECTOR = '//ul[@class="a-pagination"]/li[@class="a-last"]/a/@href'
            next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )

    def get_information(self, book):
        NAME_SELECTOR = './/span[@class="a-size-medium a-color-base a-text-normal"]/text()'
        AUTHOR_SELECTOR = './/a[@class="a-size-base a-link-normal"]/text()'
        PUBLISH_SELECTOR = './/span[@class="a-size-base a-color-secondary a-text-normal"]/text()'
        RATING_SELECTOR = './/span[@class="a-icon-alt"]/text()'
        PRICE_SELECTOR = './/span[@class="a-offscreen"]/text()'
        BADGE_SELECTOR = './/span[@class="a-badge-text"]/text()'
        # LINK_SELECTOR = './/a[contains(.//text(), \'Paperback\')]/@href'

        return {
            'name': book.xpath(NAME_SELECTOR).extract_first(),
            'author': book.xpath(AUTHOR_SELECTOR).extract_first(),
            'publish': book.xpath(PUBLISH_SELECTOR).extract_first(),
            'rating': book.xpath(RATING_SELECTOR).extract_first(),
            'price': book.xpath(PRICE_SELECTOR).extract_first(),
            'badge': book.xpath(BADGE_SELECTOR).extract_first(),
            # 'link': book.xpath(LINK_SELECTOR).extract_first(),
        }

    def write_to_file(self, information, response):
        try:
            page = response.url.split("pg_", 1)[1]
        except IndexError:
            page = 1

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        filename = self.directory + 'books-page-{0}.csv'.format(page)
        with open(filename, 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([str(information['name']) +
                             "," + str(information['author']).strip() +
                             "," + str(information['publish']) +
                             "," + str(information['rating']) +
                             "," + str(information['price']) +
                             "," + str(information['badge'])])
            writeFile.close()
