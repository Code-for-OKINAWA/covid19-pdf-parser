# pip install requests BeautifulSoup4 pdfplumber pandas pypdf2 fpdf2
from datetime import datetime,timezone,timedelta
import requests
import urllib.request
import codecs
import os
from bs4 import BeautifulSoup

import re
import sys
import pandas as pd
import time

# Retrieve html
domain = 'https://www.pref.okinawa.lg.jp'
url = domain + '/site/hoken/chiikihoken/kekkaku/press/20200214_covid19_pr1.html'
response = requests.get(url)

## Get file link and change file name
soup = BeautifulSoup(response.text, "html.parser")
link = soup.find(id="tmp_contents").find('a', href = re.compile(r'.*documents\/\d+youseisyaitiran.*'))['href']

# DOWNLOAD FILE
domain = 'https://www.pref.okinawa.lg.jp'
csv_url = domain + link

def remove_invisible_chars(chars):
    for char in chars:
        if char['non_stroking_color'] == (1,1,1):
            print(char)

def convert_to_utf8(filefolder, filename):
    # Shift_JIS ファイルのパス
    shiftjis_csv_path = filefolder + '/' + filename

    # UTF-8 ファイルのパス
    utf8_csv_path = filefolder + '/utf8_' + filename

    # 文字コードを utf-8 に変換して保存
    fin = codecs.open(shiftjis_csv_path, "r", "shift_jis")
    fout_utf = codecs.open(utf8_csv_path, "w", "utf-8")
    for row in fin:
        fout_utf.write(row)
    fin.close()
    fout_utf.close()
    os.remove(shiftjis_csv_path)
    return utf8_csv_path

def find_missing(list, rows):
    return [x for x in range(1, rows)
                               if str(x) not in list]

# Out report
report_txt = open('data/report.txt', 'w')
def print_and_write(txt):
    print(txt)
    report_txt.write(txt)
    report_txt.write('\n')


filefolder = './csv'
filename = 'all_cases.csv'
filepath = filefolder + '/' + filename

## Download the file
urllib.request.urlretrieve(csv_url, filepath)
utf8_csv = convert_to_utf8(filefolder, filename)
print("CSV downloaded at: " + filepath)

## Process CSV
csvDf = pd.read_csv(utf8_csv, sep=',', encoding="utf_8")
csvDf.columns=csvDf.columns.str.replace('\n','')
csvDf = csvDf.replace('\n','', regex=True)
csvDf = csvDf.replace('　','', regex=True)

csvDf['発病日'] = csvDf['発病日'].str.replace(r'(年|月)', '/').replace('日', '')
csvDf['発病日'] = csvDf['発病日'].str.replace('日', '')

csvDf['確定日'] = csvDf['確定日'].str.replace(r'(年|月)', '/').replace('日', '')
csvDf['確定日'] = csvDf['確定日'].str.replace('日', '')
csvDf.replace(regex=["年"], value="/", inplace=True)

indexNames = []
indexNames2 = csvDf[ csvDf['確定陽性者'] == "＊" ].index
indexNames3 = csvDf[ csvDf['確定陽性者'].isnull() ].index
indexNames4 = csvDf[ csvDf['確定陽性者'] == "" ].index
indexNames5 = csvDf[ csvDf['性別'] == "欠番" ].index
indexNames6 = csvDf[ csvDf['性別'] == "" ].index
indexNames7 = csvDf[ csvDf['性別'].isnull() ].index
indexNames8 = csvDf[ csvDf['年齢'] == "欠番" ].index
if not indexNames2.empty:
    indexNames.extend(indexNames2.to_list())
if not indexNames3.empty:
    indexNames.extend(indexNames3.to_list())
if not indexNames4.empty:
    indexNames.extend(indexNames4.to_list())
if not indexNames5.empty:
    indexNames.extend(indexNames5.to_list())
if not indexNames6.empty:
    indexNames.extend(indexNames6.to_list())
if not indexNames7.empty:
    indexNames.extend(indexNames7.to_list())
if not indexNames8.empty:
    indexNames.extend(indexNames8.to_list())
csvDf.drop(indexNames , inplace=True)

# Create a report
utcNow = datetime.utcnow().replace(tzinfo=timezone.utc)
jstNow = utcNow.astimezone(timezone(timedelta(hours=9))) # Change Timezone to JST

current_time = jstNow.strftime("%H:%M:%S")
missing_rows = find_missing(list(csvDf['確定陽性者']), int(csvDf.iat[0,0]))
print_and_write('Report created at: ' + current_time + ' JST')
print_and_write('Total cases: ' + str(len(csvDf.index)))
print_and_write('Missing cases: ' + str(len(missing_rows)))
print_and_write('Missing case id: ' + repr(missing_rows))
report_txt.close()

csvDf.to_csv('data/auto_output.csv', index=False, header=True)
print("Case CSV created at: data/auto_output.csv")