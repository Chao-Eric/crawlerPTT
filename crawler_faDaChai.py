from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
import re
import csv
from pprint import pprint
import codecs


def get_content_by_range(url_18,url,beginDate,endDate,kw):
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
        u_b_month=int(re.split('/',beginDate)[0])
        u_e_month=int(re.split('/',endDate)[0])
        u_b_date=int(re.split('/',beginDate)[1])
        u_e_date=int(re.split('/',endDate)[1])
        sucCount=0
        for div in reversed(divs):
            tmp_date=div.find('div', class_='date').get_text()
            s_month=int(re.split('/',tmp_date)[0])
            s_date=int(re.split('/',tmp_date)[1])

            #condition1: match with begin month
            if s_month==u_b_month and u_b_month!=u_e_month:
                #condition1.1: date also match
                if s_date>=u_b_date:
                    sucCount += 1
                    contentToday = {}
                    print(f'Today is {s_month}/{s_date} . Correct1')
                    # find title
                    contentToday['title'] = ''
                    if re.findall(pattern=kw,string=div.find('div', class_='title').text):
                        contentToday['title'] = cln.sub('', div.find('div', class_='title').get_text())
                        contentToday['date'] = str(s_month) + '/' + str(s_date)
                        # getting push number
                        contentToday['pushNum'] = ''
                        if div.find('span', 'hl f2'):
                            try:
                                contentToday['pushNum'] = div.find('span', 'hl f2').get_text()
                            # fail to transform
                            except ValueError:
                                pass

                        if div.find('div', 'author'):
                            contentToday['author'] = div.find('div', 'author').get_text()
                        contentAll.append(contentToday)
                    elif div.find('div', class_='title')==None:
                        print(f'NO {kw} match.')
                    else:
                        print(type(div.find('div', class_='title')))

                    if sucCount == 20:
                        urlPrev = 'https://www.ptt.cc' + bs.find('a', class_='btn wide', text='‹ 上頁').attrs['href']
                        contentAll += get_content_by_range(url_18, urlPrev, beginDate,endDate,kw)
                else:
                    print(f'Today is{div.find("div", class_="date").get_text()} date smaller than range.')
                    break

            #condition 2:match with end month
            elif s_month==u_e_month and u_b_month!=u_e_month:
                #condition 2.1:date also match
                if s_date <=u_e_date:
                    sucCount += 1
                    contentToday = {}
                    print(f'Today is {s_month}/{s_date} . Correct2')
                    # find title
                    contentToday['title'] = ''
                    if re.findall(pattern=kw,string=div.find('div', class_='title').text):
                        contentToday['title'] = cln.sub('', div.find('div',class_='title').get_text())
                        contentToday['date'] = str(s_month) + '/' + str(s_date)
                        # getting push number
                        contentToday['pushNum'] = ''
                        if div.find('span', 'hl f2'):
                            try:
                                contentToday['pushNum'] = div.find('span', 'hl f2').get_text()
                            # fail to transform
                            except ValueError as e:
                                pass

                        if div.find('div', 'author'):
                            contentToday['author'] = div.find('div', 'author').get_text()
                        contentAll.append(contentToday)

                    elif div.find('div', class_='title') == None:
                        print(f'NO {kw} match.')
                    else:
                        print(type(div.find('div', class_='title')))

                    if sucCount == 20:
                        urlPrev = 'https://www.ptt.cc' + bs.find('a', class_='btn wide', text='‹ 上頁').attrs['href']
                        contentAll += get_content_by_range(url_18, urlPrev, beginDate, endDate, kw)
                else:
                    print(f'Today is{div.find("div", class_="date").get_text()} date bigger than range.')
                    urlPrev = 'https://www.ptt.cc' + bs.find('a', class_='btn wide', text='‹ 上頁').attrs['href']
                    print(urlPrev)
                    contentAll += get_content_by_range(url_18, urlPrev, beginDate,endDate,kw)
                    break
            #condition 3: begin month and ending month are same
            elif s_month==u_b_month and s_month==u_e_month:
                if s_date>=u_b_date and s_date<=u_e_date:
                    sucCount += 1
                    contentToday = {}
                    print(f'Today is {s_month}/{s_date} . Correct3')
                    # find title
                    contentToday['title'] = ''
                    if re.findall(pattern=kw, string=div.find('div', class_='title').text):
                        contentToday['title'] = cln.sub('', div.find('div', class_='title').get_text())
                        contentToday['date'] = str(s_month) + '/' + str(s_date)
                        # getting push number
                        contentToday['pushNum'] = ''
                        if div.find('span', 'hl f2'):
                            try:
                                contentToday['pushNum'] = div.find('span', 'hl f2').get_text()
                            # fail to transform
                            except ValueError as e:
                                pass

                        if div.find('div', 'author'):
                            contentToday['author'] = div.find('div', 'author').get_text()
                        contentAll.append(contentToday)

                    elif div.find('div', class_='title') == None:
                        print(f'NO {kw} match.')
                    else:
                        print(type(div.find('div', class_='title')))

                    if sucCount == 20:
                        urlPrev = 'https://www.ptt.cc' + bs.find('a', class_='btn wide', text='‹ 上頁').attrs['href']
                        contentAll += get_content_by_range(url_18, urlPrev, beginDate, endDate, kw)
                elif s_date>u_e_date:
                    print(f'Today is{div.find("div", class_="date").get_text()} date not in range.')
                    urlPrev = 'https://www.ptt.cc' + bs.find('a', class_='btn wide', text='‹ 上頁').attrs['href']
                    print(urlPrev)
                    contentAll += get_content_by_range(url_18, urlPrev, beginDate,endDate,kw)
                    break
                elif s_date<u_b_date:
                    print(f'Today is{div.find("div", class_="date").get_text()} date smaller than range.')
                    break
            #condition 4: month between begin&end ==> match
            elif u_b_month<s_month<u_e_month:
                sucCount += 1
                contentToday = {}
                print(f'Today is {s_month}/{s_date} . Correct4')
                # find title
                contentToday['title'] = ''
                if re.findall(pattern=kw,string=div.find('div', class_='title').text):
                    contentToday['title'] = cln.sub('', div.find('div', class_='title').get_text())
                    contentToday['date'] = str(s_month) + '/' + str(s_date)
                    # getting push number
                    contentToday['pushNum'] = ''
                    if div.find('span', 'hl f2'):
                        try:
                            contentToday['pushNum'] = div.find('span', 'hl f2').get_text()
                        # fail to transform
                        except ValueError as e:
                            pass

                    if div.find('div', 'author'):
                        contentToday['author'] = div.find('div', 'author').get_text()
                    contentAll.append(contentToday)
                elif div.find('div', class_='title') == None:
                    print(f'NO {kw} match.')
                else:
                    print(type(div.find('div', class_='title')))

                if sucCount == 20:
                    urlPrev = 'https://www.ptt.cc' + bs.find('a', class_='btn wide', text='‹ 上頁').attrs['href']
                    contentAll += get_content_by_range(url_18, urlPrev, beginDate, endDate, kw)
            else:
                print(f'Today is{div.find("div", class_="date").get_text()} month not in range.')
                break

        #pprint(bs)
        return contentAll


#def faDaChai(content):



begin=input("Enter the begging date: ")
end=input("Enter the ending date: ")
kw=input("Enter the keyword you prefer to search: ")
a=get_content_by_range("https://www.ptt.cc/ask/over18","https://www.ptt.cc/bbs/Gossiping/index37438.html",begin,end,kw)

with codecs.open('fadaChai.csv','w',encoding='UTF-8') as csvFile:
    fieldnames=['date','pushNum','title','author']
    writer=csv.DictWriter(csvFile,fieldnames=fieldnames)
    writer.writeheader()
    for row in a:
        writer.writerow(row)
