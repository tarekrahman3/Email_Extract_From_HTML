import undetected_chromedriver.v2 as uc
import time
import re
import simpleaudio
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import urllib.parse
def notify():
    wave_obj = simpleaudio.WaveObject.from_wave_file("bell.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()
driver = uc.Chrome()
driver.set_page_load_timeout(20)
def dict_csv_read():
    return pd.read_csv('domains.csv').domains.tolist()

def scrape(url, index, dict_array):
    if index%50==0:
        pd.DataFrame(dict_array).to_csv('backup_data.csv', index = False)
    try:
        driver.get(url)
        emails_search = driver.execute_script(r'return Array.from(new Set(Array.from(String(document.body.innerText).matchAll(/\b[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+\b/g)).map((e)=>e.toString().trim().toLowerCase())))')
        domain_emails =[]
        other_emails = []
        emails_search = list(set([re.sub(r'^www\.|^undefined|^email|\.$','',i) for i in emails_search]))
        for i in emails_search:
            if i == 'document.authentication@det.nsw.edu.au' or i=='edweek@det.nsw.edu.au':
                pass
            else:
                if '.nsw' in i or '.edu' in i:
                    domain_emails.append(i)
                else:
                    other_emails.append(i)
    except:
        domain_emails = None
        other_emails =None
    try:
        phone_number = list(set([re.sub(r'\(|\)','',i) for i in driver.execute_script(r"return Array.from(new Set(Array.from(String(document.body.innerText).matchAll(/\(02\) \d{4} \d{4}|02 \d{4} \d{4}/g)).map((e)=>e.toString().trim())))")]))
    except:
        phone_number = None
    data = {
        'source':url,
        'domain_emails':domain_emails,
        'other_emails':other_emails,
        'phone_number':phone_number
        }
    print(f"{index} | {data}")
    dict_array.append(data)

google_search_urls = dict_csv_read()
dict_array = []
try:
    for index, url in enumerate(google_search_urls):
            time.sleep(1)
            scrape(url, index, dict_array)
except Exception as e:
    print(e)
finally:
    pd.DataFrame(dict_array).to_csv('export.csv', index = False)
driver.quit()
