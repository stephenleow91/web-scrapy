import scrapy
import csv
import logging
import os


class BrickSetSpider(scrapy.Spider):
    name = 'brick_spider'
    start_urls = ['http://brickset.com/sets/year-2019']
    directory = 'brickset/'

    def parse(self, response):
        SET_SELECTOR = '.set'

        for brickset in response.css(SET_SELECTOR):
            information = self.get_information(brickset)
            self.write_to_file(information, response)

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def get_information(self, brickset):
        NAME_SELECTOR = 'h1 ::text'
        PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
        MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
        IMAGE_SELECTOR = 'img ::attr(src)'

        return {
            'name': brickset.css(NAME_SELECTOR).extract_first(),
            'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
            'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
            'image': brickset.css(IMAGE_SELECTOR).extract_first(),
        }

    def write_to_file(self, information, response):
        try:
            page = response.url.split("page-", 1)[1]
        except IndexError:
            page = 1

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        filename = self.directory + 'brickset-page-{0}.csv'.format(page)
        with open(filename, 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([str(information['name']) + "," + str(information['pieces']) +
                             "," + str(information['minifigs']) +
                             "," + str(information['image'])])
            writeFile.close()
