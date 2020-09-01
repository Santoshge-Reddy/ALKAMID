import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json

import pandas as pd


from scrapyscript import Job, Processor

class Alkamid(scrapy.Spider):
    name = "alkamid"
    start_urls = ['http://alkamid.ugent.be/alkamidresults.php']


    def __init__(self):
        self.chemicals_details = {}
        self.chemicals_in_plants  = {}


    def parse(self, response):
        # SET_SELECTOR = '.resultstable'
        tablerows = response.xpath('//tr').getall()

        del tablerows[0]
        
        for val in tablerows:
            S_id            = '//tr/td[1]/text()'
            # SELECTOR_structure        = '//tr/td[2]/text()'
            S_chemical_name = '//tr/td[3]/text()'
            S_trivial_name  = '//tr/td[4]/text()'
            S_formula       = '//tr/td[5]/text()'
            S_origin        = '//tr/td[6]/text()'
            S_mw            = '//tr/td[7]/text()'
            

            tab = scrapy.Selector(text=val)

            trivial_name  = tab.xpath(S_trivial_name).extract()[0]
            if trivial_name:
                trivial_name = None

            plant_origin  = tab.xpath(S_origin).extract()[0]
            chemical_name = tab.xpath(S_chemical_name).extract()[0] 
            
            if chemical_name == '-':
                chemical_name = None
            

            self.chemicals_details[tab.xpath(S_chemical_name).extract()[0]] = { 
                                                                'trivial_names' : {trivial_name},
                                                                'formula': tab.xpath(S_formula).extract()[0],
                                                                'molecular_weight': tab.xpath(S_mw).extract()[0]
                                                              }
            # print(chemicals_details)

            # print(tab.xpath(S_id).extract()[0] )
            # print(tab.xpath(S_structure).extract()[0] )
            # print(tab.xpath(S_chemical_name).extract()[0] )
            # print(tab.xpath(S_trivial_name).extract()[0] )
            # print(tab.xpath(S_formula).extract()[0] )
            # print(tab.xpath(S_origin).extract()[0] )

            cip = self.chemicals_in_plants.get(plant_origin)
            # print(cip)
    

            if cip:
                # print(cip)
                plant_origin_value = cip
                plant_origin_value.add(chemical_name)
            else:
                plant_origin_value = {chemical_name}

            self.chemicals_in_plants[plant_origin] = plant_origin_value
            # print(plant_origin_value)
 
        


        NEXT_PAGE_SELECTOR = '.pagenumber.unselected a::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).getall()
        # del next_page[0]

        if next_page and len(next_page) > 0:
            next_page = next_page[0]

            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
                )
        else:

            # self.append()
            # if not os.path.exists('chemicals_details.txt'):
            #     os.makedirs('chemicals_details.txt')

            # if not os.path.exists('chemicals_in_plants.txt'):
            #     os.makedirs('chemicals_in_plants.txt')


            # f = open('C://psidw/service.txt', 'a+')

            df1 = pd.DataFrame(self.chemicals_details) 
            df2 = pd.DataFrame(self.chemicals_in_plants.items()) 

            print(df1.transpose())

            # df2.apply(lambda x: pd.Series(x[1]),axis=1).stack().reset_index(level=1, drop=True)
            print(df2)
            if not os.path.exists('C://alkamid'):
                os.makedirs('C://alkamid')


            details_file = json.dumps(str(self.chemicals_details))
            with open('C://alkamid/chemicals_details.json', 'w+') as out_file:
                out_file.write(details_file)

            plants_details_file = json.dumps(str(self.chemicals_in_plants))
            with open('C://alkamid/chemicals_in_plants.json', 'w+') as out_file:
                out_file.write(plants_details_file)


            scraped_info = {
                            'chemical_details': self.chemicals_details,
                            'chemials_in_plants': self.chemicals_in_plants
                    }


            # print(scraped_info)
            yield scraped_info


    # def append(self):
    #     # print(self.chemicals_details)
    #     # print(self.chemicals_in_plants)

    #     scraped_info = {
    #                     'chemical_details': self.chemicals_details,
    #                     'chemials_in_plants': self.chemicals_in_plants
    #             }


    #     # print(scraped_info)
    #     yield scraped_info








process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Alkamid)
process.start() 

