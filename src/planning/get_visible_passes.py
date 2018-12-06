# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 22:33:22 2018

@author: andreameraner
"""
#from urllib.request import urlopen
#import requests
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree

options = webdriver.ChromeOptions()

class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)
        
def read_webpage(day, month, year, max_mag):
    
    url='https://in-the-sky.org/satpasses.php?day='+day+'&month='+month+'&year='+year+'&mag='+max_mag+'&anysat=v0&group=1&s='
    print(url)
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    path_to_chrome_driver=r"C:\Users\andreameraner\dev\chromedriver.exe"
    browser = webdriver.Chrome(path_to_chrome_driver,options=options)
    browser.get(url)
    
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    
    passes_table = soup.find_all('tbody')[1]

    passes_info=list()
    for row_content in passes_table.find_all('tr'):
        new_row = [None]*15 #initialize None row, robust to missing values
        for col_n, col_content in enumerate(row_content.find_all('td')):
            new_row[col_n] = col_content.get_text()
        passes_info.append(new_row)
        
    return np.asarray(passes_info)
    


if __name__ == '__main__':
    
    day = 7
    month = 12
    year = 2018

    max_mag = 3

    start_time_hour = 18
    start_time_min = 00
    stop_time_hour = 23
    stop_time_min = 59
    
    passes_info = read_webpage(str(day), str(month), str(year), str(max_mag))
    print(passes_info)
    
    
    
    








