# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Product(scrapy.Item):

    product_url_didikz = scrapy.Field()
    name_didikz = scrapy.Field()
    price_didikz = scrapy.Field()

    product_url_ayutoyskz = scrapy.Field()
    name_ayutoyskz = scrapy.Field()
    price_ayutoyskz = scrapy.Field()

    price = scrapy.Field()
    price_old = scrapy.Field()
    article = scrapy.Field()


