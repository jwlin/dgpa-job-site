# 人事行政總處事求人網站開放資料版

![workflow](https://github.com/jwlin/dgpa-job-site/actions/workflows/main_wa-dgpa-d-azuw.yml/badge.svg)

將人事行政總處事求人網站每日的職缺開放資料(主要為公務人員部分)以更直覺的方式呈現，特色如下:

 - 上方的下拉式選單直接顯示本日有開缺的類科及職缺數
 - 職缺預設以職等由高到低呈現，標題只顯示必要資訊，詳細資訊可點選標題展開
 - 若該職缺近期內在事求人頻繁開缺(兩次以上)，該筆職缺下方額外顯示開缺日期
 - 提供匿名留言，除了留言內容與（亂數雜湊後的）密碼外，系統不儲存任何資訊
 - 提供各職系及各機關開缺數統計資訊列表、搜尋及排序

另，以下類別的職缺將不會顯示:

 - 不屬於銓敘部職組職系一覽表列的職系、或職系為空白
 - 「人員類別」為「約僱人員、駐外人員、代理教師、代課教師、實習老師、聘用人員」

簡單來說就是過濾掉非公務人員

## Release Notes

### 2023-09-30

* 更改留言顯示順序，並標註留言樓層
* 移除「✔同意開放簡歷」的職缺特殊條件
* 網站採用 HTTPS
* Updated Django version from 1.8 to 4.2
* Migrated the website to Azure; followed cloud-native approach

### 2019-12-18

* 增加職系職組整併後的新職組清單

### 2016-05-16

* 新增各機關開缺數查詢：先點選機關，再點選職系，最後可看到開缺細節。所有表格皆可搜尋及自由排序欄位
* 修改各職系開缺數查詢：改以表格呈現，可搜尋及自由排序欄位
* 職缺特殊條件新增「✔同意開放簡歷」，對應原總處「請注意：本職缺啟用現職應徵人員調閱簡歷功能，現職應徵者需同意開放簡歷給徵才機關調閱」條件

## Running on localhost:
This app is developed with Django.
```
pip install -r requirements.txt
python manage.py runserver
```