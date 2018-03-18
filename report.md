# 網際網路資訊檢索 作業一
##### 403410011 簡成瑑

## 資料前處理
使用python直接讀檔，
判斷每一行的前三個字元，只要是符合「@GA」、「@U:」、「@T:」、「@B:」的
就代表是metadata，要處理掉，
有的是直接跳過去不用理它，有的則是要把後半段的資料夾取出來。
```
if '@GA' in line[0:MATCH_CHAR_NUM]:
	#print('Start a record')
	pass
elif '@U:' in line[0:MATCH_CHAR_NUM]:
	#print(line[MATCH_CHAR_NUM:linelen])
	url = line[MATCH_CHAR_NUM:linelen]
elif '@T:' in line[0:MATCH_CHAR_NUM]:
   	#print(line[MATCH_WARNING: 2018-03-15T03:44:37Z
  Unable to revive connection: file://localhost:9200/

elasticsearch.min.js:10:13911
WARNING: 2018-03-15T03:44:37Z
  No living connectionsCHAR_NUM:linelen])
	title = line[MATCH_CHAR_NUM:linelen]
elif '@B:' in line[0:MATCH_CHAR_NUM]:
   	#print('Body start:\n')
	pass
else:
    #print(line)
	content = line
```
以上的程式碼中，line就是每一行的新聞資料，
只要確認好新聞的標題、網址、內文都有處理到，就可以了。

## 輸入資料給elasticsearch
運用官方的python elasticsearch api，來把新聞資料餵進去。
官方的python api非常簡單，先用`es = Elasticsearch()`將連線初始化，
接下來只需要把大量的資料，用迴圈先填好，然後再交給`_bulk()`的helper，
丟進去，跑一下就放進去elasticsearch了。
由於測試環境效能較差，所以放資料這邊，大約花了6分鐘。
```
	recordNum = len(listOfjson)
	
    actions = [
	{
	    "_index":"news",
	    "_type":"document",
	    "_id":i+id_base,
	    "_source": {
	        "title":listOfjson[i][0].decode('utf-8'),
		    "url":listOfjson[i][1].decode('utf-8'),
		    "content":listOfjson[i][2].decode('utf-8')
	    }
	}
	    for i in range(0,recordNum)
	]
	helpers.bulk(es, actions)
	id_base+=recordNum
``` 
基本上，上面的程式碼就是把每一筆新聞資料，包成一個list，再把整個檔案的新聞資料，包成另外一個list，
這樣在拿裡面的資料的時候，可以想像成是2維的資料，比較好理解。
在寫這段程式碼的時候，還遇到了unicode的解碼問題，
查了查資料才發現，需要在中文字的後面，再加上`.decode`才可以正常執行。

## 網頁界面失敗
### 使用官方javascript api卻出現無法連線的情況
照著官方文件複製貼上，結果卻出現錯誤
```
WARNING: 2018-03-15T03:44:37Z
  Unable to revive connection: file://localhost:9200/

elasticsearch.min.js:10:13911
WARNING: 2018-03-15T03:44:37Z
  No living connections
```
然而，我可以確定elasticsearch活的好好的，並且port開在9200，
因為我用curl去測試搜尋，是可以動的，但是放到網頁上，
用javascript的api呼叫下去以後，就一堆問題跑出來了。

### 不太理解如何用javascript接收json回應
照著jQuery的get函式像elasticsearch發出了一個search的請求，
結果什麼也沒發生，讓我十分不解，
再加上有前面遇到的伺服器連線問題，讓我更難以理解問題出在哪個部份。

### 網頁搜尋畫面截圖
![](./mypage.png)