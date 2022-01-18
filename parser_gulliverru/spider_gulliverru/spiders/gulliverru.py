import scrapy
import csv
from scrapy.crawler import CrawlerProcess

from config import parcer_name, input_data, add_paths

add_paths()

from items import Product
from manufacturers_countries import manufacturers_country
from settings import FEED_EXPORT_ECODING, FEED_EXPORT_FIELDS, FEED_FORMAT, FEED_URI, USER_AGENT

articles = []
prices = []
old_prices = []
manufacturers = []

check_what_is_done = []

# Opens CSV file with name inputdata.csv,
# reading articles, prices and old_prices from it and appending them to lists
with open(input_data, "r") as data:
    for i in csv.DictReader(data):

        articles.append(i["Article"])
        prices.append(i["Price"])
        old_prices.append(i["Old Price"])
        manufacturers.append(i["Manufacturers"])

# Main spider, firstly it searching through site using articles of goods,
# then, using got links, it gathering needed goods and export result to csv
class GulliverRuSpider(scrapy.Spider):
    name = parcer_name
    allowed_domains = ['gulliver.ru']
    start_urls = []

# Making list of starting urls using articles of goods
    for art in articles:
        start_urls += [f"https://www.gulliver.ru/search?q={art}"]

# Searching through site using starting urls and pass it to the 'parse_details' function
    def parse(self, response):
        link = response.css('.catalog-block__card a').xpath('@href').get()

        yield scrapy.Request(link, callback=self.parse_details, dont_filter=True)

# Parsing required data using urls from parse func
    def parse_details(self, response):
        
# Using data from site
        article = response.css('.product__article-text::text').get().replace('APT. ', '')
        raw_body = response.css('.product__description-text::text').extract()
        body = ""
        for i in raw_body:
            body += i.strip().replace('\n','</br>')
        vendor = response.css('.specifications__value--small a::text').get().replace('\n', '').strip()
    
# Formating body with required data
        if vendor in manufacturers_country:
            country = f"</br>Производитель: {manufacturers_country[vendor]}. Товар сертифицирован"
            no_country = "True"
        else:
            country = f"</br>Производитель: Китай. Товар сертифицирован"
            no_country = "False"

# Using data from inputdata.csv
        price = prices[articles.index(article)]
        price_old = old_prices[articles.index(article)]
        manufacturer = manufacturers[articles.index(article)]


# Generates an object for export
        Item = Product()

        Item["name"] = response.css('.product__name-title::text').get().lower().title().replace(' И ', ' и ')
        Item["body"] = '<div align="justify">' + body.replace('</br>                                        ', "") + "</br>" + country + '</div>'
        Item["image"] = response.css('.product__gallery-photo--big').xpath('@data-src').getall()
        Item["article"] = article
        Item["price"] = price
        Item["price_old"] = price_old
        Item["vendor"] = vendor
        Item["amount"] = "2222"
        Item["folder"] = "Hub"
        Item["product_url"] = response.url
        Item["country"] = country

# It's false if country is not in ROOT/reuse/manufacturers_countries.py
# Looks like reverse logic, but I decided that it might be more understandable
# Like, Is country in dict? : False
        Item["no_country"] = no_country

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
}

# Taking settings and starting spider through Twisted reactor
process = CrawlerProcess(settings)
process.crawl(GulliverRuSpider)
process.start()
