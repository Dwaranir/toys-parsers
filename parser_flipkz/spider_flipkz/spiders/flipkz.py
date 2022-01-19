import scrapy
import csv
import subprocess
import w3lib.html
from scrapy.crawler import CrawlerProcess

from config import parcer_name, input_data, add_paths

add_paths()

from items import Product
from manufacturers_countries import manufacturers_country
from settings import FEED_EXPORT_ECODING, FEED_EXPORT_FIELDS, FEED_FORMAT, FEED_URI, USER_AGENT, DOWNLOAD_DELAY

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
class FlipKzSpider(scrapy.Spider):
    name = parcer_name
    allowed_domains = ['flip.kz']
    start_urls = []
    iter_counter = 0

    filters = {
        1 : '8980',
        0 : 'blank'
    }

    filters_desc = {
        1 : 'Danko Toys'
    }

    company_filter = 'blank'

    print('Choose search filter by company: ')
    print(*[str(k) + ' : ' + str(v) for k,v in filters_desc.items()], sep='\n')
    user_filter_choise = int(input('\n'))
    company_filter = filters[user_filter_choise]

# Making list of starting urls using articles of goods
    if company_filter != 'blank':
        for art in articles:
            start_urls += [f"https://www.flip.kz/search?search={art}&filter-show=1&filter-i411={company_filter}"]
    else:
        for art in articles:
            start_urls += [f"https://www.flip.kz/search?search={art}"]

# Searching through site using starting urls and pass it to the 'parse_details' function
    def parse(self, response):
        link = f"https://www.flip.kz/{response.css('.p-10 a').xpath('@href').get()}" 

        yield scrapy.Request(link, callback=self.parse_details, dont_filter=True)

# Parsing required data using urls from parse func
    def parse_details(self, response):
        
# Using data from site
        
        # body = ""
        # for i in raw_body:
        #     body += i.strip().replace('\n','</br>')
        vendor = response.css('div div p a b').get().replace('<b>', '').replace('</b>', '')
        raw_body = response.css('span[itemprop="description"]::text').extract()
        body = ''.join(raw_body) 
    
# Formating body with required data
        if vendor in manufacturers_country:
            country = f"</br>Производитель: {manufacturers_country[vendor]}. Товар сертифицирован"
            no_country = "True"
        else:
            country = f"</br>Производитель: Китай. Товар сертифицирован"
            no_country = "False"

# Using data from inputdata.csv
        
        article = articles[self.iter_counter]
        price = prices[articles.index(article)]
        price_old = old_prices[articles.index(article)]
        manufacturer = manufacturers[articles.index(article)]
        self.iter_counter += 1
        


# Generates an object for export
        Item = Product()

        Item["name"] = response.css('h1 ::text').get().lower().title()
        Item["body"] = '<div align="justify">' + body + country + '</div>'
        # Item["body"] = '<div align="justify">' + body.replace('</br>                                        ', "") + "</br>" + country + '</div>'
        Item["image"] = [url.replace('//', 'https://') for url in response.css('.prod_pic a').xpath('@href').getall()]
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
'DOWNLOAD_DELAY' : DOWNLOAD_DELAY,
}

# Taking settings and starting spider through Twisted reactor
process = CrawlerProcess(settings)
process.crawl(FlipKzSpider)
process.start()

print(f'\n\n\n\n\nCrawler {parcer_name} Finished')

subprocess.call('toys-parcers.py', shell=True)