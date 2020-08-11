import sys
import pdfplumber
import pandas as pd

output_txt = open('output.csv', 'w')

with open(sys.argv[1], 'rb') as f:
	pdf = pdfplumber.open(f.name)
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
				df=pd.DataFrame(table)
				df = df.replace('\n','', regex=True)
				df.to_csv(output_txt, index=False, header=False)
