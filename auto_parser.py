# pip install requests BeautifulSoup4 pdfplumber pandas pypdf2 fpdf2
from datetime import datetime
import re
import sys
import pdfplumber
import pandas as pd

def find_missing(list, rows): 
    return [x for x in range(1, rows)  
                               if str(x) not in list] 

# Out report
report_txt = open('data/report.txt', 'w')
def print_and_write(txt):
    print(txt)
    report_txt.write(txt)
    report_txt.write('\n')

# Start to parse the PDF
filename = 'processed_latest.pdf'
output_txt = open('data/auto_output.csv', 'w')
pdf = pdfplumber.open('./pdf/' + filename)
df = pd.DataFrame(columns=["確定陽性者", "性別", "年齢", "発病日", "確定日", "居住地", "職業", "推定感染経路"])
for page in pdf.pages:
    # Start convert Table from page 1
    if page.page_number >= 1:
        # clean up the invisible text hidden by the clips
        cleanPage = page.filter(lambda obj: obj["non_stroking_color"] != (1,1,1))

        tables = cleanPage.extract_tables({
            "vertical_strategy": "text",
            "horizontal_strategy": "lines",
            "intersection_y_tolerance": 30,
            "min_words_horizontal": 2,
        })

        for table in tables:
            localDf = pd.DataFrame(table, columns=["確定陽性者", "性別", "年齢", "発病日", "確定日", "居住地", "職業", "推定感染経路"])
            localDf = localDf.replace('\n','', regex=True)

            # Remove each page's header row
            indexNames = localDf[ localDf['確定陽性者'] == "確定陽性者" ].index
            indexNames2 = localDf[ localDf['確定陽性者'] == "＊" ].index
            indexNames3 = localDf[ localDf['確定陽性者'].isnull() ].index
            indexNames4 = localDf[ localDf['確定陽性者'] == "" ].index
            indexNames5 = localDf[ localDf['性別'] == "欠番" ].index
            
            localDf.drop(indexNames , inplace=True)
            localDf.drop(indexNames2 , inplace=True)
            localDf.drop(indexNames3 , inplace=True)
            localDf.drop(indexNames4 , inplace=True)
            localDf.drop(indexNames5 , inplace=True)

            # TODO: Replace date format
            prepend_year = '2020'
            find_pattern = r"^(?P<m>\d*)月(?P<d>\d*)\D*"
            replace_pattern = lambda date: prepend_year + '/' + date.group('m') + '/' + date.group('d')
            localDf['発病日'] = localDf['発病日'].str.replace(find_pattern, replace_pattern, regex=True)
            localDf['確定日'] = localDf['確定日'].str.replace(find_pattern, replace_pattern, regex=True)
            df = df.append(localDf)

            if page.page_number == 77:
                # print(localDf.loc[21,:])
                print(localDf)

# Create a report

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
missing_rows = find_missing(list(df['確定陽性者']), len(df.index))
print_and_write('Report created at: ' + current_time + ' GMT')
print_and_write('Total cases: ' + str(len(df.index)))
print_and_write('Missing case id: ' + repr(missing_rows))
report_txt.close()

df.to_csv(output_txt, index=False, header=True)
print("CSV file created at: data/auto_output.csv")
