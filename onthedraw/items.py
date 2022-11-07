# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OnTheDrawItem(scrapy.Item):
    # define the fields for your item here like:
    files = scrapy.Field()
    file_name = scrapy.Field()
    image_urls = scrapy.Field()
