# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HtmlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    html = scrapy.Field()
    # href = scrapy.Field()
    title = scrapy.Field()
    image_urls_ful = scrapy.Field()
    image_urls_old = scrapy.Field()
