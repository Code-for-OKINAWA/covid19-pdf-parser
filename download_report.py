# pip install request BeautifulSoup4 pdfplumber pandas
import requests
import urllib.request
from bs4 import BeautifulSoup

import re
import sys
import pdfplumber
import pandas as pd

domain = 'https://www.pref.okinawa.lg.jp'
url = domain + '/site/hoken/chiikihoken/kekkaku/press/20200214_covid19_pr1.html'
response = requests.get(url)

# Get file link and change file name
soup = BeautifulSoup(response.text, "html.parser")
link = soup.find(id="tmp_contents").find_all('a')[0]['href']
filename = link[link.find('documents/')+10:].replace('hou', '_').replace('reime', '')

# Download the file
download_url = domain + link
urllib.request.urlretrieve(download_url, './pdf/' + filename)
# print(filename)

# Start to parse the PDF
output_txt = open('data/output.csv', 'w')
pdf = pdfplumber.open('./pdf/' + filename)
# df=pd.DataFrame(columns=["確定陽性者", "性別", "年齢", "発病日", "確定日", "居住地", "職業", "推定感染経路"])
df=pd.DataFrame()
for page in pdf.pages:

    # Start convert Table from page 3
    if page.page_number >= 3:
        tables = page.extract_tables({
            "vertical_strategy": "text",
            "horizontal_strategy": "lines",
            "intersection_y_tolerance": 15,
        })

        # print(tables)
        for table in tables:
            tmpDf = pd.DataFrame(table);
            print(page.page_number)
            print(tmpDf)
            # localDf = pd.DataFrame(table, columns=["確定陽性者", "性別", "年齢", "発病日", "確定日", "居住地", "職業", "推定感染経路"])
            localDf = pd.DataFrame(table)
            localDf = localDf.replace('\n','', regex=True)

            # Remove each page's header row
            # indexNames = localDf[ localDf['確定陽性者'] == "確定陽性者" ].index
            localDf.drop(indexNames , inplace=True)

            # TODO: Replace date format

            df = df.append(localDf)

df.to_csv(output_txt, index=False, header=True)

