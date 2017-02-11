'''
Arthur: Chuchuyei
Method: Crawler currency from Taiwan Bank
'''
import os
import time
import pandas as pd
from selenium import webdriver
from tqdm import tqdm
from kernel import PreprocessedData

file_path = os.path.join(os.getcwd(), 'data')
currency_source = 'current_data.xlsx'
try:
    filename = [f for f in os.listdir(file_path) if 'ExchangeRate@' in f][0]
    os.remove(os.path.join(file_path, filename))
except Exception:
    pass

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": file_path}
chromeOptions.add_experimental_option("prefs", prefs)
chromedriver = os.path.join(os.getcwd(), 'chromedriver')
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

currency = ['USD', 'HKD', 'GBP', 'AUD', 'CAD', 'SGD', 'CHF', 'JPY',
            'ZAR', 'SEK', 'NZD', 'THB', 'PHP', 'IDR', 'EUR', 'KRW',
            'VND', 'MYR', 'CNY',
            ]
p = PreprocessedData(file_path, currency_source)

with tqdm(total=len(currency)) as pbar:
    for i in currency:
        url = 'http://rate.bot.com.tw/xrt/flcsv/0/l6m/' + str(i)
        browser.get(url)
        p.current_transfer_file(i)
        pbar.update()
browser.close()
