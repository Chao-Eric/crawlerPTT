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
    else:
        return bs


def get_replied_page(url):
    try:
        cookies=requests.session()
        headers={
        #'Content - Type': 'text / plain;charset = UTF - 8',
        #'Origin': 'https: // cofacts.g0v.tw',
        #'Referer': 'https://cofacts.g0v.tw/articles?before=&after=&filter=solved',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }
        url+='?before=&after=&filter=solved&q=&replyRequestCount=1'
        r=cookies.get(url,headers=headers)
        print(f'The HTTP status is {r}')
    except HTTPError as e:
        print(e)
    else:
        bs=BeautifulSoup(r.text,'html.parser')
    return bs


def get_link_list(bs):
    linkList=[]
    result=bs.find_all('a',{'href':re.compile('\/article\//*')})
    for links in result:
        linkList.append(links.attrs['href'])
    return linkList

def get_content(links):
    contentAll=[]
    cln = re.compile(r'\n| |\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t|\r')
    for link in links:
        contentOne = {}
        bs=get_bs('https://cofacts.g0v.tw'+link)

        beforeM=bs.find('article',class_='message')
        #clean the links in message
        if beforeM.find_all("a",{'href':re.compile('http*')}):
            removes = beforeM.find_all("a",{'href':re.compile('http*')})
            for single_remove in removes:
                single_remove.extract()

        #clean the links contents in the message
        if beforeM.find_all("section",class_="links"):
            removes = beforeM.find_all("section",class_="links")
            for single_remove in removes:
                single_remove.extract()
        contentOne['text'] = cln.sub('', beforeM.get_text())
        contentOne['label']=label_trans(bs.find('strong').get_text())
        pos=int(bs.find_all('span',class_='vote-num')[0].get_text())
        neg=int(bs.find_all('span',class_='vote-num')[1].get_text())
        contentOne['feedBack'] = pos-neg
        contentAll.append(contentOne)
    return contentAll


def label_trans(label):
    if label!='':
        if re.findall('不在查證範圍',label)!=[]:
            label = 'NOT_ARTICLE'
        elif re.findall('含有個人意見', label)!=[]:
            label = 'OPINIONATED'
        elif re.findall('含有正確訊息',label)!=[]:
            label = 'FACT'
        elif re.findall('含有不實訊息', label)!=[]:
            label = 'RUMOR'
    else:
        print('emptyLabel')
    return label


def get_all(dbUrl,contentAll):
    linkList = get_link_list(get_replied_page(dbUrl))
    pprint(linkList)
    bs=get_replied_page(dbUrl)
    #print(bs)
    contentAll.append(get_content(linkList))
    pprint(f'This is contentall now ==> {contentAll}')
    # ab=bs.find("a",text="Next").attrs['href']
    # print(f'This is Next URL: {ab}')
    if bs.find('a',text='Prev') is None:
        #condition 1 : first page
        if bs.find('a', text='Next') is not None:
            print('condition1')
            nextUrl = 'https://cofacts.g0v.tw/articles' + bs.find('a',text='Next').attrs['href']
            print(f'Next URL: {nextUrl}')
            contentAll.append(get_all(nextUrl,contentAll))
        elif bs.find('a', text='Next') is None:
            print('Both None ==> program error')
            return contentAll
    elif bs.find('a', text='Prev') is not None:
        #condition 2 : last page
        if bs.find('a', text='Next') is None:
            print('condition2')
            return contentAll
        #condition 3 : others
        elif bs.find('a', text='Next') is not None:
            print('condition3')
            nextUrl = 'https://cofacts.g0v.tw/articles' + bs.find('a', text='Next').attrs['href']
            print(f'Next URL: {nextUrl}')
            contentAll.append(get_all(nextUrl,contentAll))



url='https://cofacts.g0v.tw/'
dbUrl=url+get_bs(url).find('a',text='謠言資料庫').attrs['href']
contentAll=[]
a=get_all(dbUrl,contentAll)

with codecs.open('G0V.csv','w',encoding='UTF-8') as csvFile:
    fieldnames=['feedBack','label','text','date']
    writer=csv.DictWriter(csvFile,fieldnames=fieldnames)
    writer.writeheader()
    for row in a:
        writer.writerow(row)