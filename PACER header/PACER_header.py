import os
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
import unicodedata

# get local directory, find html documents
# produce absolute path for scraping
file_path = os.getcwd()

html_files = list(filter(lambda x: '.html' in x, os.listdir(file_path)))

local_path = 'file:///' + file_path + '/'
new_html_path = [local_path + x for x in html_files]


# final output format
header = {'Case': [], 'Status': [], 'Judge': []}


# scraping starts here
class PacerSpider(scrapy.Spider):
    name = 'pacer_header_spider'
    
    def start_requests(self):
        urls = new_html_path
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
    
    def parse(self, response):
        # scrape case title, status, judge name and dates
        case_title = response.css('div#cmecfMainContent > center:nth-of-type(1) ::text').extract()
        for i in range(len(case_title)):
            case_title[i] = case_title[i].replace('\r\n', ' ')
        header['Case'].append(case_title[2])

        case_status = response.css('div#cmecfMainContent').xpath('table[1]//h2//text()').extract()
        for i in range(len(case_status)):
            case_status[i] = case_status[i].replace('\r\n', ' ')
            case_status[i] = unicodedata.normalize("NFKD", case_status[i]).strip()
        
        if '' in case_status:
            case_status.remove('')
        header['Status'].append(case_status[-1])
        
        judge_name = response.css('div#cmecfMainContent').xpath('table[2]/tr/td[1]//text()').extract()
        for i in range(len(judge_name)):
            judge_name[i] = judge_name[i].replace('\r\n', ' ')
            judge_name[i] = unicodedata.normalize("NFKD", judge_name[i]).strip()
        
        if '' in judge_name:
            judge_name.remove('')
        header['Judge'].append(judge_name[1])

        dates = response.css('div#cmecfMainContent').xpath('table[2]/tr/td[2]//text()').extract()

        for i in range(len(dates)):
            dates[i] = unicodedata.normalize("NFKD", dates[i]).strip()

        if '' in dates:
            dates.remove('')

        # check whether date info exists in header
        # create entries for new date info
        for i in range(0, len(dates), 2):
            if dates[i] not in header:
                header[dates[i]] = [''] * (len(header['Case'])-1)
                header[dates[i]].append(dates[i+1])
            else:
                header[dates[i]].append(dates[i+1])

        # add new date info in header
        for key in header:
            if key not in dates and key not in ['Case', 'Status', 'Judge']:
                header[key].append('')
      

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

process.crawl(PacerSpider)
process.start()

# transform header into dataframe
header_df = pd.DataFrame.from_dict(header)
header_df.to_csv('PACER_header.csv', index=False)

print('Finished scraping PACER header information. Saved CSV file in local directory.')



