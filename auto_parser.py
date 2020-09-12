# pip install requests BeautifulSoup4 pdfplumber pandas pypdf2 fpdf2
from datetime import datetime,timezone,timedelta
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
output_cases = open('data/auto_output.csv', 'w')
output_summary = 'data/auto_summary.csv'

pdf = pdfplumber.open('./pdf/' + filename)
df = pd.DataFrame(columns=["確定陽性者", "性別", "年齢", "発病日", "確定日", "居住地", "職業", "推定感染経路"])
for page in pdf.pages:
    # Start convert Summary from page 1
    if page.page_number == 1:
        # bounding_box = (50, 405, 360, 710)
        bounding_box = (60, 330, 320, 610)
        page_crop = page.within_bbox(bounding_box)

        # page_crop.to_image(resolution=200).save("./snapshot/summary_crop.png", format="PNG")

        table_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "snap_tolerance": 3,
        }

        summaryTable = page_crop.extract_table(table_settings)
    # Start convert Table from page 2
    if page.page_number >= 2:
        # clean up the invisible text hidden by the clips
        # print(page.chars)
        cleanPage = page.filter(lambda obj: obj["non_stroking_color"] not in [1, (1,1,1)])

        tables = cleanPage.extract_tables({
            "vertical_strategy": "text",
            "horizontal_strategy": "lines",
            "intersection_y_tolerance": 100,
            "min_words_horizontal": 2,
        })

        for table in tables:
            localDf = pd.DataFrame(table, columns=["確定陽性者", "性別", "年齢", "発病日", "確定日", "居住地", "職業", "推定感染経路"])
            localDf = localDf.replace('\n','', regex=True)

            # Remove each page's header row
            indexNames = []
            indexNames1 = localDf[ localDf['確定陽性者'] == "確定陽性者" ].index
            indexNames2 = localDf[ localDf['確定陽性者'] == "＊" ].index
            indexNames3 = localDf[ localDf['確定陽性者'].isnull() ].index
            indexNames4 = localDf[ localDf['確定陽性者'] == "" ].index
            indexNames5 = localDf[ localDf['性別'] == "欠番" ].index
            indexNames6 = localDf[ localDf['性別'] == "" ].index
            indexNames7 = localDf[ localDf['性別'].isnull() ].index
            indexNames8 = localDf[ localDf['年齢'] == "欠番" ].index

            if not indexNames1.empty:
                indexNames.extend(indexNames1.to_list())
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

            localDf.drop(indexNames , inplace=True)

            # TODO: Replace date format
            prepend_year = '2020'
            find_pattern = r"^(?P<m>\d*)月(?P<d>\d*)\D*"
            replace_pattern = lambda date: prepend_year + '/' + date.group('m') + '/' + date.group('d')
            localDf['発病日'] = localDf['発病日'].str.replace(find_pattern, replace_pattern, regex=True)
            localDf['確定日'] = localDf['確定日'].str.replace(find_pattern, replace_pattern, regex=True)
            df = df.append(localDf)

            # if page.page_number == 61:
            #     # print(localDf.loc[21,:])
            #     print(localDf)

# Create a report
utcNow = datetime.utcnow().replace(tzinfo=timezone.utc)
jstNow = utcNow.astimezone(timezone(timedelta(hours=9))) # Change Timezone to JST

current_time = jstNow.strftime("%H:%M:%S")
missing_rows = find_missing(list(df['確定陽性者']), int(df.iat[0,0]))
print_and_write('Report created at: ' + current_time + ' JST')
print_and_write('Total cases: ' + str(len(df.index)))
print_and_write('Missing case id: ' + repr(missing_rows))
report_txt.close()

print(summaryTable)
# Save the summary CSV
current_time = jstNow.strftime("%Y/%m/%d %H:%M")
today = jstNow.strftime("%Y/%m/%d")
data = [
    current_time,
    summaryTable[14][1],
    summaryTable[1][1],
    summaryTable[3][3],
    summaryTable[4][3],
    summaryTable[5][1],
    summaryTable[6][1],
    summaryTable[7][1],
    summaryTable[9][1],
    summaryTable[10][2],
    summaryTable[11][2],
    summaryTable[12][1]
]
data = [item.replace('※', '') for item in data]
csvDf = pd.read_csv(output_summary, sep=',', encoding="utf-8")
indexNames = csvDf[ csvDf['更新時間'].str.contains(today) ].index
csvDf.drop(indexNames , inplace=True)
csvDf.loc[len(csvDf)] = data
csvDf.to_csv(output_summary, index=False)
print("Summary CSV created at: data/auto_summary.csv")

# Save the cases CSV
df.to_csv(output_cases, index=False, header=True)
print("Case CSV created at: data/auto_output.csv")
