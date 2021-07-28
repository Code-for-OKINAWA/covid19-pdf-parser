
# pip install requests BeautifulSoup4 pdfplumber pandas pypdf2 fpdf2
from datetime import datetime,timezone,timedelta
import re
import sys
import pdfplumber
import pandas as pd

# Start to parse the PDF
filename = 'processed_latest.pdf'
output_summary = 'data/auto_summary.csv'

pdf = pdfplumber.open('./pdf/' + filename)
page = pdf.pages[0]
# Start convert Summary from page 1

# bounding_box = (50, 405, 360, 710)
bounding_box = (50, 280, 320, 500)
page_crop = page.within_bbox(bounding_box)

# page_crop.to_image(resolution=200).save("./snapshot/summary_crop.png", format="PNG")

table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 3,
}
# im = page_crop.to_image(resolution=200)
# im.reset().draw_hline(780, stroke='black', stroke_width=3)
# im.debug_tablefinder(table_settings)
# im.save("./snapshot/summary.png", format="PNG")

summaryTable = page_crop.extract_table(table_settings)


print(summaryTable)
# Save the summary CSV
utcNow = datetime.utcnow().replace(tzinfo=timezone.utc)
jstNow = utcNow.astimezone(timezone(timedelta(hours=9))) # Change Timezone to JST

current_time = jstNow.strftime("%Y/%m/%d %H:%M")
today = jstNow.strftime("%Y/%m/%d")
data = [
    current_time,
    summaryTable[15][1],
    summaryTable[1][1],
    summaryTable[3][3],
    summaryTable[4][3],
    summaryTable[5][1],
    summaryTable[6][1],
    summaryTable[7][1],
    summaryTable[10][1],
    summaryTable[11][2],
    summaryTable[12][2],
    summaryTable[13][1]
]
data = [item.replace('※', '') for item in data]
csvDf = pd.read_csv(output_summary, sep=',', encoding="utf-8")
indexNames = csvDf[ csvDf['更新時間'].str.contains(today) ].index

if int(summaryTable[14][1]) != int(csvDf.loc[len(csvDf)-1].iat[1]):
    csvDf.drop(indexNames , inplace=True)
    csvDf.loc[len(csvDf)] = data
    csvDf.to_csv(output_summary, index=False)
    print("Summary CSV updated at: data/auto_summary.csv")
else:
    print("No Summary update")
