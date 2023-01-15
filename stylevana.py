import scrapy
import scrapy
import json
import os
import re
from urllib.parse import urljoin

import scrapy

class stylevanaSpider(scrapy.Spider):
    name = 'stylevana'
    sort_index = 4
    custom_settings = {
        "FEEDS": {
            os.path.join("scrapy_output", "test.csv"): {
                "format": "csv",
                "overwrite": True,
            }
        },
        
    }
    
 

    def start_requests(self):
       
        
       
        start_urls = ['https://www.stylevana.com/en_US/ryo-hair-damage-care-nourishing-conditioner-550ml.html']
        for url in start_urls:
           
            yield scrapy.Request(url=url,callback=self.parse_category_page)

         

    def parse_category_page(self, response):
        self.logger.info(f"Product category page sub page found {response.url}")
       
        products_links = response.css(".product-image::attr(href)").getall()
        products_links = [urljoin(response.url, link) for link in products_links]
        self.logger.info(f"{len(products_links)} products found in {response.url}")

        



        products_links=['https://www.stylevana.com/en_US/laneige-lip-sleeping-mask-ex-3g-berry-2ea-set.html']
        for link in products_links:
          
            yield scrapy.Request(link,headers=headers,cookies=cookies, callback=self.parse_product_page)

        # next_link=response.css('.i-next::attr(href)').get()
        # if next_link:
        #     yield scrapy.Request(next_link, callback=self.parse_category_page)
        #     print(next_link)

    def parse_product_page(self, response):
        self.logger.info(f"Product page found {response.url}")
        print(response.url)

        json_data = response.css('script::text').getall()
        # i=0
        # for data in json_data:
        #     print(data)
        #     i=i+1
        #     print("==========================")
        #     print(i)

        data=json_data[27]



      

        try:
            final_price=re.findall('data-pp-amount="([^"]+)',response.text)[0]
        except:
            final_price=""
        try:
            price=re.findall('price"\\sid="old-price-[^"]+">([^<]+)',response.text)[0].split('\n')[1]
        except:
            price=""
        try:
            name=re.findall('product-name-h1">([^<]+)',response.text)[0]
        except:
            name=""
        try:
            upc=re.findall('data-product-upc="([^"]+)',response.text)[0]
        except:
            upc=""
        try:
            stock=re.findall('final_price":[\\d\\.]+,"stock":"([^"]+)',response.text)[0]
        except:
            stock=""
        
        try:
            brand=re.findall('"brand":{"@type":"Brand","name":"([^"]+)"},',response.text)[0]
        except:
            brand=""
        
        print(price)
        print(final_price)
        print(name)
        print(upc)
        print(brand)
        print(stock)


        item = {}
        item["price"] = price
        item["final_price"] = final_price
        item["name"] =name
        item["upc"] = upc
        item["stock"] = stock
        item['brand']=brand
        item["url"] = response.url

        yield item
      

        print("-------------------------------- ")