# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# XY_WebScraper.py
# Created on: 2022-12-15
# Updated on: 2022-12-16
#
# Author: Andrew Parkin/GIS Manager
#
# Description:
# Takes our address points and runs them through Google to scrape XY data. Which will then be analysed and help correct
# our addresses in google to help eliminate resident complaints that google has their address wrong.
#
# ***REQUIREMENT besides needing selenium library you also need to download the webdriver for your web browser***
#
# ---------------------------------------------------------------------------

from selenium import webdriver
from tqdm.notebook import tqdm_notebook
import pandas as pd
from selenium.webdriver.common.by import By
import csv
from pathlib import Path

# Variables

pd.set_option('display.max_columns', 10)
address_excel_filepath = r"R:\GIS\Addresses.xls"
addresses = pd.read_excel(address_excel_filepath, keep_default_na=False)
Url_With_Coordinates = []
url_coord = r"C:\Users\baseb\Downloads\google_url_coord.csv"

option = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images':2, 'javascript':2}}
option.add_experimental_option('prefs', prefs)
option.add_argument('headless')

# Change link to work machine location
driver = webdriver.Chrome("C:\\Users\\baseb\\Downloads\\chromedriver_win32\\chromedriver.exe", options=option)

# Formatting for Dataframe
get_ipython().run_cell_magic('HTML', '', '<style>.dataframe th{background: rgb(63,87,124);background: '
                                         'linear-gradient(180deg, rgba(63,87,124,1) 0%, rgba(101,124,161,1) 100%, '
                                         'rgba(0,212,255,1) 100%);;\npadding: 10px;font-family: monospace;font-size: '
                                         '110%;color: white;border:1px dashed white;text-align:left !important;'
                                         '\n-moz-border-radius: 3x;-webkit-border-radius: 3px;}.'
                                         'dataframe thead{border:none; !important;}style>')

# adding URL field using for loop to iterate through each address.

addresses['Url'] = ['https://www.google.com/maps/search/' + i for i in addresses['Full Address']]

# Web scraping google for each address. tqdm is a status bar great for large datasets. Export results into a csv.
# In case it crashes. I did experience random crashes I couldn't explain. So ended up running in batches of around 5k.

for url in tqdm_notebook(addresses.Url, leave=False):
    driver.get(url)
    Url_With_Coordinates.append(driver.find_element(By.CSS_SELECTOR, 'meta[itemprop=image]').get_attribute('content'))

driver.close()

# Exports to CSV

with open(url_coord, 'w') as file:
    wr = csv.writer(file)
    wr.writerow(Url_With_Coordinates)

# Some addresses have weird formatting and cant be run through the process. Next two lines basically deletes the records
# that don't match the proper formatting.

addresses[~addresses.Url_With_Coordinates.str.contains('&zoom=')]

addresses = addresses[addresses.Url_With_Coordinates.str.contains('&zoom=')].copy()

# These two lines split the string to extract lat and longs as two separate fields.

addresses['lat'] = [ url.split('?center=')[1].split('&zoom=')[0].split('%2C')[0] for url in addresses['Url_With_Coordinates'] ]
addresses['long'] = [url.split('?center=')[1].split('&zoom=')[0].split('%2C')[1] for url in addresses['Url_With_Coordinates'] ]

# Exports the results to a CSV to be loaded into arcpro.

filepath = Path(r"C:\Users\baseb\Downloads\AddressOutput.csv")
filepath.parent.mkdir(parents=True, exist_ok =True)

addresses.to_csv(filepath)
