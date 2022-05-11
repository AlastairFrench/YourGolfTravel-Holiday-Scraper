#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 20:25:34 2022

@author: Alastair
"""
#import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import re

#Using webdriver and Selenium to access the webpage
DRIVER_PATH = '/Users/Alastair/Desktop/python/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

url ="https://www.yourgolftravel.com/date/12/09/2022/golf-holidays/spain/nights/5-7/rounds/5-14#js-search-title"
driver.get(url)

#get HTML document
page = driver.execute_script('return document.body.innerHTML')

#Convert HTML page to BeautifulSoup object 
soup = BeautifulSoup(''.join(page), 'html.parser')

#select only the 'offers'
results = soup.find(id="offers")

#inspect results so far
print(results.prettify())

#find the offers by selectiong only the 'ul' with a data components
offers = results.findAll('ul', attrs={'data-component' : True})
print(offers)

def parse_offers(offer):
    """
    Take in a li tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in offer.find_all('li', limit=5)]

#parse offers and turn into a list
list_of_parsed_offers = [parse_offers(offer) for offer in offers[0:]]

#turn list into a dataframe
df = DataFrame(list_of_parsed_offers)

#remove rows that didnt have details of holidays
df = df[df[0].str.contains('signature collection')==False]
df = df[df[0].str.contains('Early Booking Discount')==False]

#extract the prices from the results
prices = results.find_all('strong')
print(prices)

#turn into a list
prices_list = []
for x in prices:
    prices_list.append(str(x))
    
#remove things like £ from prices and make integers
prices_int = [(re.sub("[^0-9]", "", price)) for price in prices_list]
prices_int = [int(i) for i in prices_int]

#add price to dataframe
df.insert(0,'price', prices_int)

#save as xlsx
df.to_excel(r'/Users/Alastair/Desktop/python/golf/golf holiday scrape portugal sept 3.xlsx', index = False)



