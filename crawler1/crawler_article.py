from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
import re
from pprint import pprint
import codecs
from selenium import webdriver


def get_content(url_18,url):
    # storing cookies
    cookies = requests.session()
    # post solving config problem
    over_18 = {'from': '/bbs/Gossiping/index.html',
               'yes': 'yes'
               }
    try:
        r1 = cookies.post(url_18, data=over_18)
        r2 = cookies.get(url)
    except HTTPError as e:
        print(e)
    try:
        bs = BeautifulSoup(r2.text, 'html.parser')
    except AttributeError as e:
        print(e)
    else:
        contentList=[]
        contentDict={}
        resList=[]
        cln = re.compile(r'\n| |\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t|\r')
        # get div content
        print(bs.find_all('span', class_='article-meta-value'))
        contentDict['author']=bs.find_all('span', class_='article-meta-value')[0].get_text()
        contentDict['title']=bs.find_all('span', class_='article-meta-value')[2].get_text()
        contentDict['time']=bs.find_all('span', class_='article-meta-value')[3].get_text()
        main_content=bs.find('div',id='main-content')
        # get response
        for pushes in bs.find_all('div',class_="push"):
            resDict={}
            resDict['pushTag']=pushes.span.get_text()
            resDict['pushID']=pushes.find('span',class_='f3 hl push-userid').get_text()
            resDict['pushContent']=pushes.find('span',class_='f3 push-content').get_text()
            resDict['pushtime']=cln.sub('',pushes.find('span',class_='push-ipdatetime').get_text())
            resList.append(resDict)
        #remove tag from tree
        removes = main_content.find_all("div", class_= "article-metaline")
        for single_remove in removes:
            single_remove.extract()
        removes = main_content.find_all("div", class_="article-metaline-right")
        for single_remove in removes:
            single_remove.extract()
        removes = main_content.find_all("span", class_= "f2")
        for single_remove in removes:
            single_remove.extract()
        removes = main_content.find_all("div", class_="push")
        for single_remove in removes:
            single_remove.extract()
        contentDict['articleContent']=cln.sub(' ',main_content.get_text())
        contentList.append(contentDict)
        contentList.append(resList)
        pprint(contentList)

    return contentList


#url = input("Enter URL You Prefer to get content with:")
a=str(get_content("https://www.ptt.cc/ask/over18","https://www.ptt.cc/bbs/Gossiping/M.1563182049.A.2EC.html"))
with codecs.open('article.txt','w',encoding='UTF-8') as textFile:
    for row in a:
        textFile.write(row)
