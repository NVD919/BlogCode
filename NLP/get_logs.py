from selenium import webdriver
from bs4 import BeautifulSoup, Comment
import time 
import random

browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice

f = open('chatloglist.txt').readlines();
out_file = open('chat_logs_all_9.txt','w')

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

for line in f:
    streamer = line.split(' ')[1];

    url = "https://overrustlelogs.net/" + streamer+"%20chatlog/"
    time.sleep(2)
    browser.get(url) #navigate to the page

    innerHTML = browser.execute_script("return document.body.innerHTML") 
    soup = BeautifulSoup(innerHTML,'html.parser')
    for month in soup.find_all('a',attrs={"class":"collection-item"},href=True):
        month_url = "https://overrustlelogs.net"+month['href'].replace(' ','%20')
        time.sleep(2)
        browser.get(month_url)
        out_file.write( month_url+'\n')

        
        month_innerHTML = browser.execute_script("return document.body.innerHTML")
        month_soup = BeautifulSoup(month_innerHTML,'html.parser')
        
        for day in month_soup.find_all('a',attrs={"class":"collection-item"},href=True):
            if(hasNumbers(day['href'][-7:])):
                day_url = "https://overrustlelogs.net"+day['href'].replace(' ','%20')
                time.sleep(2)
                browser.get(day_url)

                day_innerHTML = browser.execute_script("return document.body.innerHTML")
                day_soup = BeautifulSoup(day_innerHTML,'html.parser')

                for row in day_soup.find_all('div',attrs={"class" : "text"}):
                    out_file.write( row.text.encode('utf-8'))
