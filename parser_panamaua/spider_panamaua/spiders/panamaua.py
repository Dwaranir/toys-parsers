import scrapy
import csv
import subprocess
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
with open(input_data, "r", encoding="utf8") as data:
    for i in csv.DictReader(data):

        articles.append(i["Article"])
        prices.append(i["Price"])
        old_prices.append(i["Old Price"])
        manufacturers.append(i["Manufacturers"])

def filters_choices():
    vendor_filter = {
            1 : ['Danko Toys', 27453],
        }

    company_filter_url = 'blank'

    print('Choose search filter by company: ')
    print(*[str(k) + ' : ' + str(v[0]) for k,v in vendor_filter.items()], sep='\n')
    user_filter_choice = int(input('\n'))

    company_filter_url = vendor_filter[user_filter_choice][1]
    company_name = vendor_filter[user_filter_choice][0]

    print(vendor_filter[user_filter_choice])

    s_filters = {
        'vendor': [company_name, company_filter_url]
    }

    print(s_filters)

    return s_filters

search_filters = filters_choices()

# Main spider, firstly it searching through site using articles of goods,
# then, using got links, it gathering needed goods and export result to csv
class PanamaUaSpider(scrapy.Spider):
    name = parcer_name
    allowed_domains = ['panama.ua']
    start_urls = []

# Making list of starting urls using articles of goods
    for art in articles:
        start_urls += [f"https://panama.ua/search/?q={art}#o[103][]={search_filters['vendor'][1]}&search={art}&"]

# Searching through site using starting urls and pass it to the 'parse_details' function
    def parse(self, response):
        link = 'https://panama.ua/' + response.css('.product__link').xpath('@href').get()

        yield scrapy.Request(link, callback=self.parse_details, dont_filter=True)

# Parsing required data using urls from parse func
    def parse_details(self, response):
        
# Using data from site
        article = response.css('[itemprop="sku"] ::text').get()
        raw_body = response.css('[itemprop="description"] p').extract()
        body = ""
        vendor = response.css('[itemprop="brand"] a ::text').get()
        for i in raw_body:
            body += i
        
    
# Formating body with required data
        # if vendor in manufacturers_country:
        #     country = f"</br>Производитель: {manufacturers_country[vendor]}. Товар сертифицирован"
        #     no_country = "True"
        # else:
        #     country = f"</br>Производитель: Китай. Товар сертифицирован"
        #     no_country = "False"
        
        country = 'Товар сертифицирован'
        no_country = 'False'

# Using data from inputdata.csv
        price = prices[articles.index(article)]
        price_old = old_prices[articles.index(article)]
        manufacturer = manufacturers[articles.index(article)]


# Generates an object for export
        Item = Product()

        Item["name"] = response.css('.product-item__name::text').get().replace(f' - {vendor}', '')
        Item["body"] = '<div align="justify">' + body + "</br>" + country + '</div>'
        Item["image"] = response.css('.product__gallery-page-item img').xpath('@src').getall()
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
process.crawl(PanamaUaSpider)
process.start()

print(f'\n\n\n\n\nCrawler {parcer_name} Finished')

subprocess.call('toys-parcers.py', shell=True)