import undetected_chromedriver.v2 as uc
import time
import re
from selenium.webdriver.common.by import By
import pandas as pd

def dict_csv_read():
    return pd.read_csv('import.csv').to_dict('records')

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
        emails = list(set(emails))
    except:
        emails = None
    try:
        phone_number = list(set([re.sub(r'\(|\)','',i) for i in driver.execute_script(r"return Array.from(new Set(Array.from(String(document.body.innerText).matchAll(/\(02\) \d{4} \d{4}|02 \d{4} \d{4}/g)).map((e)=>e.toString().trim())))")]))
    except:
        phone_number = None
    data = {
        'source':url,
        'domain_emails':emails,
        'phone_number':phone_number
        }
    print(f"{index} | {data}")
    dict_array.append(data)

def for_single_address():
    dict_array = []
    try:
        for index, url in enumerate(import_):
            time.sleep(1)
            scrape(url, index, dict_array)
    except Exception as e:
        print(e)
    finally:
        pd.DataFrame(dict_array).to_csv('export_type_single.csv', index = False)


def for_google_search_result():
    dict_array = []
    try:
        for index, each_dict in enumerate(import_):
            first_search_result_url = list(each_dict.values())[3]
            if str(first_search_result_url) != 'nan':
                scrape(first_search_result_url, index, dict_array)
    except Exception as e:
        print(e)
    finally:
        pd.DataFrame(dict_array).to_csv('export_type_google_search.csv', index = False)

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.set_page_load_timeout(20)
    import_ = dict_csv_read()
    print(len(import_))
    #for_single_address()
    for_google_search_result()
    driver.quit()
