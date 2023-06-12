# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 22:33:22 2018

@author: andreameraner
"""

import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import urllib.request as request
import re
import os
from tqdm import tqdm
import argparse
import time
import datetime

def get_browser(show_webpage):
    options = webdriver.ChromeOptions()
    if not show_webpage:
        options.add_argument('headless') #makes it invisible. Comment to see webpage displayed
    options.add_argument('window-size=1200x600')
    options.add_argument('log-level=3')

    if os.name == 'nt':
        print('Windows Chromedriver selected')
        path_to_chrome_driver=r"chromedriver.exe"
    elif os.name == 'posix':
        print('Linux Chromedriver selected')
        path_to_chrome_driver=r"./chromedriver"
    else:
        raise OSError('OS Not recognized')
    print("Opening Chrome webdriver")
    browser = webdriver.Chrome(path_to_chrome_driver, options=options)
    
    return browser


def get_passes_info_table(day, month, year, max_mag, show_webpage):
    
    url='https://in-the-sky.org/satpasses.php?day='+day+'&month='+month+'&year='+year+'&mag='+max_mag+'&anysat=v0&group=1&s=&gs=gs'
    print("Getting pass information from: ",url)

    browser = get_browser(show_webpage)
    
    print("Waiting for webpage to load")
    browser.get(url)
    
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    print("Webpage opened and read, now getting table")

    passes_table = soup.find_all('tbody')[1]
    #print(passes_table)
    
    passes_info=list()
    for row_content in passes_table.find_all('tr'):
        new_row = [None]*17 
        for col_n, col_content in enumerate(row_content.find_all('td')):
            new_row[col_n] = col_content.get_text()
            if col_n == 0:
                link = col_content.find('a')
                if link is None:
                    a=1
                new_row[15] = link.get('href')
            if col_n == 14:
                link = col_content.find('a')
                new_row[14] = link.get('href')
                new_row[16] = re.sub("[^0-9]", "",new_row[14][-5:])
        passes_info.append(new_row)
    
    location = soup.find_all('p', attrs={'sidebarheading'})[0]
    location = location.find('b').get_text()
    
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Got pass information table!")
    print("Location set to: ", location)
    print("Number of visible passes found: ", len(passes_info))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    
    return np.asarray(passes_info)


def save_passes_info_table(day, month, year, max_mag, passes_info_table):
    
    filenamecsv = year + month + day + "passes_maxmag" + max_mag + ".csv"
    with open(filenamecsv, 'w',newline='') as f:
        csv.writer(f, delimiter =';',).writerows(passes_info_table)
    print("Wrote passes information to csv file: ", filenamecsv)
    
    filenametxt = year + month + day + "passes_maxmag" + max_mag + ".txt"
    np.savetxt(filenametxt, passes_info_table, delimiter=" ", fmt='%s',)
    print("Wrote passes information to txt file: ", filenametxt)
    return


def get_TLEs(day, month, year, max_mag, passes_info_table, progress_bar):
    
    celestrak_baseurl = 'http://celestrak.com/cgi-bin/TLE.pl?CATNR='
    tles_filename = year + month + day + "passes_maxmag" + max_mag + "_TLE.txt"

    norad_id_list = passes_info_table[:,16]
    seen = set()
    uniq_ids = [str(x) for x in norad_id_list if x not in seen and not seen.add(x)]
    print('Number of unique NORAD IDs found: ', len(uniq_ids))

    print("Downloading and writing TLEs")
    f = open(tles_filename, "w+")
    if progress_bar == True:
        iterate = tqdm(uniq_ids)
    else:
        iterate = uniq_ids

    for norad_id in iterate:

        url = celestrak_baseurl + norad_id
        with request.urlopen(url, timeout=20) as celestrakpage:
            tle = celestrakpage.read()
            
        tlesoup = BeautifulSoup(tle,features="lxml")
        tletext = tlesoup.get_text()
        tletextstart = tletext.find("\n\r\n")+3 #find start of tle (ignore name)
        f.write(tlesoup.get_text()[tletextstart:tletextstart+170])
        
    f.close()
    print("Wrote all passes TLEs to: ", tles_filename)

    return


if __name__ == '__main__':

    today = datetime.date.today()
    
    parser = argparse.ArgumentParser(description='Get visible passes information')
    parser.add_argument('--day', action='store', dest='day', default=today.day, help='Day of observation')
    parser.add_argument('--month', action='store', dest='month', default=today.month, help='Month of observation')
    parser.add_argument('--year', action='store', dest='year', default=today.year, help='Year of observation')
    parser.add_argument('--max_mag', action='store', dest='max_mag', default=5, help='Maximum magnitude of objects. Default 5. Set 500 for all illuminated objects')
    parser.add_argument('--silent_webpage', action='store_false', dest='show_webpage', default=False, help='Show opened webpage in browser')
    parser.add_argument('--show_progressbar', action='store_true', dest='show_progressbar', default=True, help='Show progress bar when loading TLEs')

    args = parser.parse_args()

    start = time.time()
    print('Starting download at', time.ctime())

    passes_info_table = get_passes_info_table(str(args.day), str(args.month), str(args.year), str(args.max_mag), args.show_webpage)

    save_passes_info_table(str(args.day), str(args.month), str(args.year), str(args.max_mag), passes_info_table) 
    get_TLEs(str(args.day), str(args.month), str(args.year), str(args.max_mag), passes_info_table, args.show_progressbar)
    
    print("\n\nSUCCESS\n\n")
    print('Elapsed time: ', time.time() - start)
    print('Ending time: ', time.ctime())
    
