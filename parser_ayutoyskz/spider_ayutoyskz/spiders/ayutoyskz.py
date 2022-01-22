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

names_didikz = []
prices_didikz = []
products_url_didikz = []

# Opens CSV file with name inputdata.csv,
# reading articles, prices and old_prices from it and appending them to lists
with open(input_data, "r", encoding='utf-8') as data:
    for i in csv.DictReader(data):

        articles.append(i["article"])
        prices.append(i["price"])
        old_prices.append(i["price_old"])

        names_didikz.append(i["name_didikz"])
        prices_didikz.append(i["price_didikz"])
        products_url_didikz.append(i["product_url_didikz"])


# Main spider, firstly it searching through site using articles of goods,
# then, using got links, it gathering needed goods and export result to csv
class AyutoysKzSpider(scrapy.Spider):
    name = parcer_name
    allowed_domains = ['ayutoys.kz']
    start_urls = []
    iter_counter = 0

# Making list of starting urls using articles of goods
    for art in articles:
        start_urls += [f"https://ayutoys.kz/site_search?search_term={art}"]

# Searching through site using starting urls and pass it to the 'parse_details' function
    def parse(self, response):
        link = response.css('.cs-goods-title').xpath('@href').get()
        
        if link == None:

            article = articles[self.iter_counter]
            price = prices[articles.index(article)]
            price_old = old_prices[articles.index(article)]

            price_didikz = prices_didikz[articles.index(article)]
            name_didikz = names_didikz[articles.index(article)]
            product_url_didikz = products_url_didikz[articles.index(article)]

            Item = Product()
        
            Item["article"] = article
            Item["price"] = price
            Item["price_old"] = price_old
            Item["price_didikz"] = price_didikz
            Item["name_didikz"] = name_didikz
            Item["product_url_didikz"] = product_url_didikz
            Item["price_ayutoyskz"] = ' '
            Item["name_ayutoyskz"] = ' '
            Item["product_url_ayutoyskz"] = ' '

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
            Item["price_ayutoyskz"] = response.css('[data-qaid="product_price"] ::text').get().encode("utf-8").decode('unicode_escape').encode('ascii', 'ignore')
            Item["name_ayutoyskz"] = response.css('[data-qaid="product_name"] ::text').get()
            Item["product_url_ayutoyskz"] = response.url
        
        else:
            article = articles[self.iter_counter]
            Item["price_ayutoyskz"] = Item["name_ayutoyskz"] = Item["product_url_ayutoyskz"] = ' '
        
        place_in_dict = articles.index(article)

        price = prices[place_in_dict]
        price_old = old_prices[place_in_dict]
        price_didikz = prices_didikz[place_in_dict]
        name_didikz = names_didikz[place_in_dict]
        product_url_didikz = products_url_didikz[place_in_dict]
            
        Item["article"] = article
        Item["price"] = price
        Item["price_old"] = price_old
    
        Item["price_didikz"] = price_didikz
        Item["name_didikz"] = name_didikz
        Item["product_url_didikz"] = product_url_didikz

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
process.crawl(AyutoysKzSpider)
process.start()

print(f'\n\n\n\n\nCrawler {parcer_name} Finished')

# subprocess.call('toys-parcers.py', shell=True)