import scrapy
import csv
import subprocess
from scrapy.crawler import CrawlerProcess

from config import parcer_name, input_data, add_paths

add_paths()

from items import Product
from settings import FEED_EXPORT_ECODING, FEED_EXPORT_FIELDS, FEED_FORMAT, FEED_URI, USER_AGENT, DOWNLOAD_DELAY

articles = []
prices = []
old_prices = []

with open(f'{parcer_name}_result.csv', "w") as data:
    print(f'{parcer_name}_result.csv cleaned')
# Opens CSV file with name inputdata.csv,
# reading articles, prices and old_prices from it and appending them to lists
with open(input_data, "r") as data:
    for i in csv.DictReader(data):

        articles.append(i["Article"])
        prices.append(i["Price"])
        old_prices.append(i["Old Price"])

# Main spider, firstly it searching through site using articles of goods,
# then, using got links, it gathering needed goods and export result to csv
class DidiKzSpider(scrapy.Spider):
    name = parcer_name
    allowed_domains = ['di-di.kz']
    start_urls = []
    iter_counter = 0

# Making list of starting urls using articles of goods
    for art in articles:
        start_urls += [f"https://di-di.kz/site_search?search_term={art}"]

# Searching through site using starting urls and pass it to the 'parse_details' function
    def parse(self, response):
        link = response.css('.cs-product-gallery__title a').xpath('@href').get()
        
        if link == None:

            article = articles[self.iter_counter]
            price = prices[articles.index(article)]
            price_old = old_prices[articles.index(article)]

            Item = Product()
        
            Item["article"] = article
            Item["price"] = price
            Item["price_old"] = price_old
            Item["price_didikz"] = ' '
            Item["name_didikz"] = ' '
            Item["product_url_didikz"] = ' '

            self.iter_counter += 1

            yield Item
        
        else:
            self.iter_counter += 1

            yield scrapy.Request(link, callback=self.parse_details, dont_filter=True)

# Parsing required data using urls from parse func
    def parse_details(self, response):

        Item = Product()

        article = response.css('.b-product-data__item_type_sku span ::text').get().strip()

        if article in articles:
            Item["price_didikz"] = response.css('[data-qaid="product_price"] ::text').get().encode("utf-8").decode('unicode_escape').encode('ascii', 'ignore')
            Item["name_didikz"] = response.css('[data-qaid="product_name"]::text').get()
            Item["product_url_didikz"] = response.url
        
        else:
            article = articles[self.iter_counter]
            Item["price__didikz"] = Item["name__didikz"] = Item["product_url__didikz"] = ' '
        
        place_in_dict = articles.index(article)

        price = prices[place_in_dict]
        price_old = old_prices[place_in_dict]
        
            
        Item["article"] = article
        Item["price"] = price
        Item["price_old"] = price_old

        yield Item

# Settings for easy script run, mirroring settings from setting.py
# get_project_settings() from scrapy official doc didn't work
# it returns link to the memory, not the object
settings = {
'FEED_FORMAT' : FEED_FORMAT,
'FEED_EXPORT_ECODING': FEED_EXPORT_ECODING,
'FEED_URI' : FEED_URI,
'FEED_EXPORT_FIELDS' : FEED_EXPORT_FIELDS,
'USER_AGENT' : USER_AGENT,
'DOWNLOAD_DELAY' : DOWNLOAD_DELAY,
}

# Taking settings and starting spider through Twisted reactor
process = CrawlerProcess(settings)
process.crawl(DidiKzSpider)
process.start()

print(f'\n\n\n\n\nCrawler {parcer_name} Finished')

# subprocess.call('toys-parcers.py', shell=True)