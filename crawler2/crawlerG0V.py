from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
import re
import csv
from pprint import pprint
import codecs
from  selenium import webdriver
import time

def get_bs(url):
    try:
        cookies = requests.session()
        html=cookies.get(url)
    except HTTPError as e:
        print(e)
    try:
        bs=BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print(e)
    return bs


def get_replied_page(url):
    try:
        cookies=requests.session()
        headers={
        'Content - Type': 'text / plain;charset = UTF - 8',
        'Origin': 'https: // cofacts.g0v.tw',
        'Referer': 'https://cofacts.g0v.tw/articles?before=&after=&filter=solved',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }
        url+='?before=&after=&filter=solved&q=&replyRequestCount=1'
        r=cookies.get(url,headers=headers)
    except HTTPError as e:
        print(e)
    else:
        bs=BeautifulSoup(r.text,'html.parser')
    return bs


def get_link_list(bs):
    linkList=bs.find_all('a',{'href':re.compile('\/article\/*')})
    for links in linkList:
        print(links.attrs['href'])

url='https://cofacts.g0v.tw/'
dbUrl=url+get_bs(url).find('a',text='謠言資料庫').attrs['href']
#pprint(get_replied_page(dbUrl).find_all('li'))
get_link_list(get_replied_page(dbUrl))