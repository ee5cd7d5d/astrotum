# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 22:33:22 2018

@author: andreameraner
"""
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from selenium import webdriver



def read_webpage(day, month, year, min_mag):
    
    #link = "https://in-the-sky.org/satpasses.php?day=2&month=12&year=2018&mag=5&anysat=v0&group=1&s="
    #link = "https://www.heavens-above.com/AllSats.aspx?lat=48.1495&lng=11.5673&loc=80333+Monaco+di+Baviera%2c+Germania&alt=516&tz=CET&cul=en"
    #webpage = urlopen(link)
    
#    #return webpage.read()
#    # the target we want to open     
    url='https://in-the-sky.org/satpasses.php?day=2&month=12&year=2018&mag=5&anysat=v0&group=1&s='
#      
#    #open with GET method 
#    resp=requests.get(url) 
#      
#    #http_respone 200 means OK status 
#    if resp.status_code==200: 
#        print("Successfully opened the web page") 
#        print("The news are as follow :-\n") 
#      
#        # we need a parser,Python built-in HTML parser is enough . 
#        soup=BeautifulSoup(resp.text,'html.parser')     
#  
#        # l is the list which contains all the text i.e news  
#        lll=soup.find("div",{"class":"mainpage container"}) 
#      
#        #now we want to print only the text part of the anchor. 
#        #find all the elements of a, i.e anchor 
#        for i in lll.findAll("a"): 
#            print(i.text) 
#    else: 
#        print("Error")
#        
#    return
    path_to_chrome_driver=r"C:\Users\andreameraner\dev\chromedriver.exe"
    browser = webdriver.Chrome(path_to_chrome_driver)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    a = soup.find_all('tr')
    print(a)
    
    return
    


if __name__ == '__main__':
    
    day = 2
    month = 12
    year = 2018

    min_mag = 3

    start_time_hour = 18
    start_time_min = 00
    stop_time_hour = 23
    stop_time_min = 59
    
    webpage_content = read_webpage(day, month, year, min_mag)
    print(webpage_content)
    
    
    
    








