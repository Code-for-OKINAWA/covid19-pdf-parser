# pip install requests BeautifulSoup4 pdfplumber pandas pypdf2 fpdf2
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader

from datetime import datetime
import re
import sys
import pdfplumber
import pandas as pd

# Out report
summary_csv = open('data/auto_summary.csv', 'a')
def print_and_write(txt):
    print(txt)
    summary_csv.write(txt)
    summary_csv.write('\n')

filename = '78_1867.pdf'
# --- Create lines
linePDF = FPDF()
linePDF.add_page(orientation='P', format='A4')
linePDF.set_fill_color(0,0,0)
linePDF.rect(21, 123.5, 0.25, 91,'F')
linePDF.set_fill_color(0,0,0)
linePDF.rect(58.5, 123.5, 0.25, 91,'F')
linePDF.set_fill_color(0,0,0)
linePDF.rect(72, 123.5, 0.25, 91,'F')
linePDF.set_fill_color(0,0,0)
linePDF.rect(92, 123.5, 0.25, 79,'F')
linePDF.set_fill_color(0,0,0)
linePDF.rect(99, 123.5, 0.25, 79,'F')

linePDF.set_fill_color(0,0,0)
linePDF.rect(21, 208, 51, 0.25,'F')
linePDF.set_fill_color(0,0,0)
linePDF.rect(21, 214, 51, 0.25,'F')

linePDF.output('component/line_summary_table.pdf', 'F')

# --- Add lines to every page
outputPDF = PdfFileWriter()
sourcePDF = PdfFileReader(open('./pdf/' + filename, "rb"))
linePDF = PdfFileReader(open("component/line_summary_table.pdf", "rb"))

page0 = sourcePDF.getPage(0)
page0.mergePage(linePDF.getPage(0))
outputPDF.addPage(page0)
## --- finally, write "outputPDF" to document-outputPDF.pdf
outputPDFStream = open('./pdf/processed_summary.pdf', "wb")
outputPDF.write(outputPDFStream)

print ('PDF summary preprocess finished')

# --- Start to parse the PDF
# filename = '74_1690.pdf'

pdf = pdfplumber.open('./pdf/processed_summary_copy.pdf')

page0 = pdf.pages[0]
bounding_box = (50, 330, 285, 610)
page_crop = page0.within_bbox(bounding_box)

page_crop.to_image(resolution=200).save("./summary_crop.png", format="PNG")

table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 3, 
}
im = page_crop.to_image(resolution=200)
im.reset().draw_hline(780, stroke='black', stroke_width=3)
im.debug_tablefinder(table_settings)
im.save("summary.png", format="PNG")

table = page_crop.extract_table(table_settings)

# --- Create a status summary CSV
now = datetime.now()
current_time = now.strftime("%Y/%m/%d %H:%M")
today = now.strftime("%Y/%m/%d")
# print_and_write("更新時間, 県関係者陽性者数, 入院中, 重症, 中等症, 入院調整中, 宿泊施設療養中, 自宅療養中, 入院勧告解除, 解除後再入院,　退院, 死亡退院")
print(table)
data = [
    current_time, 
    table[14][1], 
    table[1][1], 
    table[1][3], 
    table[2][3],
    table[5][1], 
    table[6][1], 
    table[7][1], 
    table[9][1], 
    table[10][2], 
    table[11][2], 
    table[12][1]
]

data = [item.replace('※', '') for item in data]
# print_and_write(', '.join(data))
# summary_csv.close()

# -- Append to summary CSV

csvDf = pd.read_csv("data/auto_summary.csv", sep=',', encoding="utf-8")
indexNames = csvDf[ csvDf['更新時間'].str.contains(today) ].index
print(indexNames)
csvDf.drop(indexNames , inplace=True)
csvDf.loc[len(csvDf)] = data
csvDf.to_csv("data/auto_summary.csv", index=False)
