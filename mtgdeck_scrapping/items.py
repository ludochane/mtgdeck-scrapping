# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DeckItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    finish = scrapy.Field()
    player = scrapy.Field()
    event = scrapy.Field()
    format = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    maincards = scrapy.Field()
    sideboard = scrapy.Field()
    url = scrapy.Field()

class CardItem(scrapy.Item):
    name = scrapy.Field()
    occurrence = scrapy.Field()
