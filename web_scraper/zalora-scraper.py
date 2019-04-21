import scrapy
import csv
import logging
import os
import json
import re


class ZaloraClawler(scrapy.Spider):
    name = "zalora_clawler"
    start_urls = ['https://www.zalora.com.my/levis/']

    def parse(self, response):
        data = re.findall("app.settings =(.+?);",
                          response.body.decode("utf-8"), re.S)
        ls = []

        formattedData = data[0].replace('\'', '"')

        with open("zalora.txt", 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([formattedData])
            writeFile.close()

        if data:
            ls = json.loads(formattedData)

        if ls:
            print(ls)
        else:
            print("empty----------------------")
