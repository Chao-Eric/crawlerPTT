# crawlerPTT
---
## crawler_content.py

+ 功能 : 爬取輸入日期當日的所有文章之 推文數(pushNum)+標題(title)+發文日期(date)+作者ID(author)
+ 輸入格式 : 月份/日期
  + 例 :
  ```
  Enter The Date You Prefer to search:7/14
  ```
+ 輸出檔案格式 : CSV(content.csv)
+ 結果部份圖 :
  ![image](https://github.com/Chao-Eric/crawlerPTT/blob/master/img/content_result.PNG)


---
## crawler_faDaChai.py

+ 功能 : 爬取輸入日期範圍之輸入字串的文章 =>> 推文數(pushNum)+標題(title)+發文日期(date)+作者ID(author)
+ 輸入格式 : 輸入起始日期,終止日期+欲查詢字串
  + 例 :
  ```
       Enter the begging date:7/30
       Enter the ending date:7/31
       Enter the keyword you prefer to search:問卦
  ```
+ 輸出檔案格式: CSV(faDaChai.csv)
+ 結果部分圖 :
    ![image](https://github.com/Chao-Eric/crawlerPTT/blob/master/img/faDaChai_result.PNG)

---
## crawler_article.py

+ 功能: 爬取特定文章之內容:
  + 作者(author)
  + 時間(time)
  + 標題(title)
  + 內文(articleContent)
  + 回應(推(pushTag)+回覆者ID(pushID)+回覆內容(pushContent)+回覆IP和時間(pushTime))
+ 輸出檔案格式: TXT(article.txt)
+ 結果部分圖 : 
  ![image](https://github.com/Chao-Eric/crawlerPTT/blob/master/img/article_result_1.PNG)
  ![image](https://github.com/Chao-Eric/crawlerPTT/blob/master/img/article_result_2.PNG)
                             
