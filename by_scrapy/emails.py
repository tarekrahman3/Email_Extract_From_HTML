import scrapy
import pandas as pd
import re

import_data = pd.read_csv('import.csv').to_dict('records')

class EmailsSpider(scrapy.Spider):
    name = 'emails'
    allowed_domains = [re.sub(r'^http:\/\/www\.|^https:\/\/www\.|^https:\/\/|^http:\/\/|^www\.|\/$|/.+','',each_row['url']) for each_row in import_data]
    start_urls = [each_row['url'] for each_row in import_data]

    def parse(self, response):
        final_emails = []
        try:
            emails = list(set(re.findall(r'\b[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+\b',str(response.body))))
            if len(emails)>0:
                for ex in emails:
                    if str(type(re.search(r'jpg$|jpeg$|png$|svg$|\.js|\.css|\.webp|bootstrap|@\d{1,2}\.\d{1,2}', ex.lower())))!="<class 're.Match'>":
                        if ex == '' or re.match(r'^x', ex) or re.match(r'0x|sentry', ex) or re.match(r'@.\.\.$|@.\.\.\.$', ex) or len(re.sub('@.+','',ex))>31:
                            pass
                        else:
                            final_emails.append(ex)
        except Exception as e:
            print(str(e))
        
        yield {
            'url': response.request.url,
            'emails': final_emails
        }
