import sys
import pdfplumber
import pandas as pd

output_txt = open('output.csv', 'w')
output_txt2 = open('output2.csv', 'w')

with open(sys.argv[1], 'rb') as f:
	pdf = pdfplumber.open(f.name)
	df=pd.DataFrame(columns=["確定陽性者", "性別", "年齢", "発病日", "確定日", "居住地", "職業", "推定感染経路"])
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
				localDf=pd.DataFrame(table, columns=["確定陽性者", "性別", "年齢", "発病日", "確定日", "居住地", "職業", "推定感染経路"])
				localDf = localDf.replace('\n','', regex=True)
				indexNames = localDf[ localDf['確定陽性者'] == "確定陽性者" ].index
				localDf.drop(indexNames , inplace=True)
				df = df.append(localDf)
	
	df.to_csv(output_txt, index=False, header=True)

