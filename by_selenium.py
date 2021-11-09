import undetected_chromedriver.v2 as uc
import time
import re
from selenium.webdriver.common.by import By
import pandas as pd

def dict_csv_read():
    return pd.read_csv('domains.csv').domains.tolist()

def scrape(url, index, dict_array):
    if index%50==0:
        pd.DataFrame(dict_array).to_csv('backup_data.csv', index = False)
    try:
        driver.get(url)
        emails_search = driver.execute_script(r'return Array.from(new Set(Array.from(String(document.body.innerText).matchAll(/\b[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+\b/g)).map((e)=>e.toString().trim().toLowerCase())))')
        emails = []
        emails_search = list(set([re.sub(r'^www\.|^undefined|^email|\.$','',i) for i in emails_search]))
        [emails.append(i) for i in emails_search]
        e = driver.execute_script(r' return Array.from(new Set(Array.from(String(document.documentElement.outerHTML).matchAll(/\b[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+\b/g)).map((e)=>e.toString().trim().toLowerCase())))')
        [emails.append(i) for i in e]
    except:
        emails = None
    try:
        phone_number = list(set([re.sub(r'\(|\)','',i) for i in driver.execute_script(r"return Array.from(new Set(Array.from(String(document.body.innerText).matchAll(/\(02\) \d{4} \d{4}|02 \d{4} \d{4}/g)).map((e)=>e.toString().trim())))")]))
    except:
        phone_number = None
    data = {
        'source':url,
        'domain_emails':list(set(emails)),
        'phone_number':phone_number
        }
    print(f"{index} | {data}")
    dict_array.append(data)

driver = uc.Chrome()
driver.set_page_load_timeout(20)
urls = dict_csv_read()
dict_array = []
try:
    for index, url in enumerate(urls):
            time.sleep(1)
            scrape(url, index, dict_array)
except Exception as e:
    print(e)
finally:
    pd.DataFrame(dict_array).to_csv('export.csv', index = False)
    driver.quit()
