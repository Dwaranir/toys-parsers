# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):

    product_url = scrapy.Field()
    name = scrapy.Field()
    body = scrapy.Field()
    image = scrapy.Field()
    article = scrapy.Field()
    price = scrapy.Field()
    price_old = scrapy.Field()
    vendor = scrapy.Field()
    amount = scrapy.Field()
    folder = scrapy.Field()
    country = scrapy.Field()
    no_country = scrapy.Field()


