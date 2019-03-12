# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 22:33:22 2018

@author: andreameraner
"""

import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import urllib.request
import re
import os
from tqdm import tqdm
import argparse
import time
import datetime


def get_browser(show_webpage):
    options = webdriver.ChromeOptions()
    if not show_webpage:
        options.add_argument('headless')  # makes it invisible. Comment to see webpage displayed
    options.add_argument('window-size=1200x600')
    options.add_argument('log-level=3')

    if os.name == 'nt':
        print('Windows Chromedriver selected')
        path_to_chrome_driver = r"chromedriver.exe"
    elif os.name == 'posix':
        print('Linux Chromedriver selected')
        path_to_chrome_driver = r"./chromedriver"
    else:
        raise OSError('OS Not recognized')
    print("Opening Chrome webdriver")
    browser = webdriver.Chrome(path_to_chrome_driver, options=options)

    return browser


def get_table_from_site(day, month, year, max_mag, show_webpage):
    url = 'https://in-the-sky.org/satpasses.php?day=' + day + '&month=' + month + '&year=' + year + '&mag=' + max_mag + '&anysat=v0&group=1&s='
    print("Getting pass information from: ", url)

    browser = get_browser(show_webpage)

    print("Waiting for webpage to load")
    browser.get(url)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    print("Webpage opened and read, now getting table")

    passes_table = soup.find_all('tbody')[1]
    # print(passes_table)

    location = soup.find_all('p', attrs={'centretext'})[0]
    location = location.find('b').get_text()

    return passes_table, location


def read_passes_table_to_ndarray(passes_table, max_mag_input):
    passes_info = list()

    for row_content in passes_table.find_all('tr'):
        new_row = [None] * 17
        disregard_line = False
        for col_n, col_content in enumerate(row_content.find_all('td')):
            new_row[col_n] = col_content.get_text()
            if col_n == 0:
                link = col_content.find('a')
                new_row[15] = link.get('href')
            if col_n == 14:
                link = col_content.find('a')
                new_row[14] = link.get('href')
                new_row[16] = re.sub("[^0-9]", "", new_row[14][-5:])
            if col_n == 9:
                try:  # check if mag is a number
                    mag = int(new_row[col_n])
                except:
                    try:  # extract number and disregard question mark
                        mag = int(re.search(r'\d+', new_row[col_n]).group())
                    except:  # catch missing number
                        disregard_line = True
                        continue

                if mag > int(max_mag_input):
                    disregard_line = True
                    continue
                else:
                    new_row[col_n] = mag

        if not disregard_line:
            passes_info.append(new_row)

    for vis_pass in passes_info:
        del vis_pass[1]

    return passes_info


def get_next_day_date(day, month, year):
    date = datetime.datetime(int(year), int(month), int(day))
    date += datetime.timedelta(days=1)
    return str(date.day), str(date.month), str(date.year)


def get_passes_info_table(day, month, year, max_mag_input, show_webpage):
    if int(max_mag_input) > 5:
        print("Maximum magnitude is bigger than 5. Retrieving all visible passes first and filter later.")
        max_mag = str(500)
    else:
        max_mag = max_mag_input

    (passes_table, location) = get_table_from_site(day, month, year, max_mag, show_webpage)
    passes_info = read_passes_table_to_ndarray(passes_table, max_mag_input)

    # filter morning passes
    passes_info = [vis_pass for vis_pass in passes_info if int(re.search(r'\d+', vis_pass[1]).group()) >= 12]

    (day, month, year) = get_next_day_date(day, month, year)
    (passes_table_nextday, location) = get_table_from_site(day, month, year, max_mag, show_webpage)
    passes_info_nextday = read_passes_table_to_ndarray(passes_table_nextday, max_mag_input)

    # filter evening passes
    passes_info_nextday = [vis_pass for vis_pass in passes_info_nextday if
                           int(re.search(r'\d+', vis_pass[1]).group()) < 12]

    passes_info += passes_info_nextday

    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Got pass information table!")
    print("Location set to: ", location)
    print("Number of visible passes found: ", len(passes_info))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    return np.asarray(passes_info)


def save_passes_info_table(day, month, year, max_mag, passes_info_table, data_path):
    # add first explanatory line
    column_description = ['Object Name', 'Start Time', 'Start Dir', 'Start El', 'Start Magnitude', 'Highest Time',
                          'Highest Dir', 'Highest El', 'Highest Magnitude', 'End Time', 'End Dir', 'End El',
                          'End Magnitude', 'Pass Information', 'Object Information', 'Object ID']

    passes_info_table = np.vstack([column_description, passes_info_table])

    filenamecsv = year + month + day + "passes_maxmag" + max_mag + ".csv"
    filenamecsv = os.path.join(data_path, filenamecsv)
    with open(filenamecsv, 'w', newline='') as f:
        csv.writer(f, delimiter=';', ).writerows(passes_info_table)
    print("Wrote passes information to csv file: ", filenamecsv)

    filenametxt = year + month + day + "passes_maxmag" + max_mag + ".txt"
    filenametxt = os.path.join(data_path, filenametxt)
    np.savetxt(filenametxt, passes_info_table, delimiter=" ", fmt='%s' )
    print("Wrote passes information to txt file: ", filenametxt)

    return


def get_TLEs(day, month, year, max_mag, passes_info_table, progress_bar, data_path):
    celestrak_baseurl = 'http://celestrak.com/cgi-bin/TLE.pl?CATNR='

    tles_filename = year + month + day + "passes_maxmag" + max_mag + "_TLE.txt"
    tles_filename = os.path.join(data_path, tles_filename)

    norad_id_list = passes_info_table[:, 15]
    seen = set()
    uniq_ids = [str(x) for x in norad_id_list if x not in seen and not seen.add(x)]
    print('Number of unique NORAD IDs found: ', len(uniq_ids))

    print("Downloading and writing TLEs")
    f = open(tles_filename, "w+")
    if progress_bar:
        iterate = tqdm(uniq_ids)
    else:
        iterate = uniq_ids

    for norad_id in iterate:
        url = celestrak_baseurl + norad_id
        with urllib.request.urlopen(url) as celestrakpage:
            tle = celestrakpage.read()

        tlesoup = BeautifulSoup(tle, features="lxml")
        tletext = tlesoup.get_text()
        tletextstart = tletext.find("\n\r\n") + 3  # find start of tle (ignore name)
        f.write(tlesoup.get_text()[tletextstart:tletextstart + 170])

    f.close()
    print("Wrote all passes TLEs to: ", tles_filename)

    return


def date_str(nr):
    return str(nr).zfill(2)


def get_visible_passes_routine(day, month, year, max_mag=5, show_webpage=False, show_progressbar=False,
                               dont_save_table=False, dont_save_TLEs=False):
    base_out_path = 'passes_data'
    foldername = date_str(year) + date_str(month) + date_str(day)
    data_path = os.path.join(base_out_path, foldername)
    if not os.path.isdir(data_path):
        os.makedirs(data_path)

    start = time.time()
    print('Retrieving passes for the night of %d/%d/%d:' % (day, month, year))
    print('Maximum magnitude set to ', max_mag)
    print('Starting download at', time.ctime())

    passes_info_table = get_passes_info_table(date_str(day), date_str(month), date_str(year),
                                              date_str(max_mag), show_webpage)

    if not dont_save_table:
        save_passes_info_table(date_str(day), date_str(month), date_str(year), date_str(max_mag),
                               passes_info_table, data_path)

    if not dont_save_TLEs:
        get_TLEs(date_str(day), date_str(month), date_str(year), date_str(max_mag), passes_info_table,
                 show_progressbar, data_path)

    print("\n***********\nSUCCESS\n***********\n")
    print('Elapsed time: ', time.time() - start)
    print('Ending time: ', time.ctime())

    return


if __name__ == '__main__':
    
    now = datetime.datetime.now()

    parser = argparse.ArgumentParser(description='Get visible passes information')
    parser.add_argument('--day', action='store', dest='day', default=now.day, help='Day of observation')
    parser.add_argument('--month', action='store', dest='month', default=now.month, help='Month of observation')
    parser.add_argument('--year', action='store', dest='year', default=now.year, help='Year of observation')
    parser.add_argument('--max_mag', action='store', dest='max_mag', default=5,
                        help='Maximum magnitude of objects. Set 500 for all illuminated objects')
    parser.add_argument('--show_webpage', action='store_true', dest='show_webpage', default=False,
                        help='Show opened webpage in browser')
    parser.add_argument('--show_progressbar', action='store_true', dest='show_progressbar', default=False,
                        help='Show progress bar when loading TLEs')
    parser.add_argument('--dont_save_table', action='store_true', dest='dont_save_table', default=False,
                        help='Do not save table file')
    parser.add_argument('--dont_save_TLEs', action='store_true', dest='dont_save_TLEs', default=False,
                        help='Do not save the TLEs')

    args = parser.parse_args()

    get_visible_passes_routine(args.day, args.month, args.year, args.max_mag, args.show_webpage, args.show_progressbar,
                               args.dont_save_table, args.dont_save_TLEs)
