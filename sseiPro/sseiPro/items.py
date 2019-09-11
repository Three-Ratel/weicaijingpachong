# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SseiproItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    opening_price = scrapy.Field()
    highest_price = scrapy.Field()
    bottom_price = scrapy.Field()
    closing_price = scrapy.Field()
    turnover = scrapy.Field()


