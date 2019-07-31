from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
import re
import csv
from pprint import pprint
import codecs

def get_content_by_date(url_18,url,date):
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
        contentAll=[]
        cln=re.compile(r'\n| |\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t|\r')
        #get div content
        divs=bs.find_all('div',class_='r-ent')
        u_month=int(re.split('/',date)[0])
        u_date=int(re.split('/',date)[1])
        sucCount=0
        for div in reversed(divs):
            tmp_date=div.find('div', class_='date').get_text()
            s_month=int(re.split('/',tmp_date)[0])
            s_date=int(re.split('/',tmp_date)[1])

            #condition1: date match
            if s_month==u_month and s_date==u_date:
                sucCount+=1
                contentToday = {}
                print(f'Today is {s_month}/{s_date} . Correct')
                contentToday['date']=date

                #getting push number
                contentToday['pushNum']=''
                if div.find('span','hl f2'):
                    try:
                        contentToday['pushNum']=div.find('span','hl f2').get_text()
                    #fail to transform
                    except ValueError as e:
                        pass
                #find title
                contentToday['title']=''
                if div.find('div','title'):
                    contentToday['title'] = cln.sub('',div.find('div','title').get_text())
                if div.find('div','author'):
                    contentToday['author']=div.find('div','author').get_text()
                contentAll.append(contentToday)
                if sucCount==20:
                    urlPrev = 'https://www.ptt.cc' + bs.find('a', class_='btn wide', text='‹ 上頁').attrs['href']
                    contentAll += get_content_by_date(url_18, urlPrev, date)

            #condition 2:bigger than date wanted
            elif s_month>u_month or s_month==u_month and s_date>u_date :
                print(f'Today is{div.find("div", class_="date").get_text()} bigger')
                urlPrev='https://www.ptt.cc'+bs.find('a',class_='btn wide',text='‹ 上頁').attrs['href']
                print(urlPrev)
                contentAll+=get_content_by_date(url_18,urlPrev,date)
                break
            #condition 3:smaller than date wanted
            elif s_month<u_month or s_month==u_month and s_date<u_date:
                print(f'Today is{div.find("div", class_="date").get_text()} smaller.')
                break
        return contentAll



Sdate = input("Enter The Date You Prefer to search:")
a=get_content_by_date("https://www.ptt.cc/ask/over18","https://www.ptt.cc/bbs/Gossiping/index38862.html",Sdate)
with codecs.open('content.csv','w',encoding='UTF-8') as csvFile:
    fieldnames=['date','pushNum','title','author']
    writer=csv.DictWriter(csvFile,fieldnames=fieldnames)
    writer.writeheader()
    for row in a:
        writer.writerow(row)


