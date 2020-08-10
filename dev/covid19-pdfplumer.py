import pdfplumber
pdf = pdfplumber.open("../pdf/064_968.pdf")
import pandas as pd

output_txt = open('output.txt', 'w')

def rects_to_edges(rects):
	edges = []
	for rect in rects:
		edges += pdfplumber.utils.rect_to_edges(rect)
	return edges

# img = pdf.pages[3].to_image(resolution=150)
# img.save('screenshot.png')
for page in pdf.pages:
	if page.page_number == 5:
		for key, value in page.objects.items():
			print(key, len(value))
		page.to_image(resolution=200).draw_lines(page.rects).save("./rects.png", format="PNG")

	if page.page_number == 5:
		# print(page.width, page.height)
		# print(page.objects)
		page_crop = page.crop([80,50,550,880])
		exp_hline = rects_to_edges(page.rects)
		print(len(exp_hline))
		page.to_image(resolution=200).draw_lines(exp_hline).save("./line.png", format="PNG")

		tables = page_crop.find_tables({
			    "vertical_strategy": "text", 
			    "horizontal_strategy": "lines",
			    "text_tolerance": 10,
			    "min_words_vertical": 2,
			    # "explicit_horizontal_lines": rects_to_edges(page.rects)
			    "snap_tolerance": 8,
			    # "edge_min_length": 10
		})
		print(tables)
		page_crop.to_image(resolution=200).debug_table(tables[0]).save("./deb.png", format="PNG")

		table_debug = page.debug_tablefinder({
			"vertical_strategy": "text",
			"horizontal_strategy": "lines"
		})

		page.to_image(resolution=200).debug_tablefinder().save("./deb2.png", format="PNG")
		print(table_debug)

	if page.page_number == 5:
		words = page.extract_words()
		# print(words)

	if page.page_number == 5:
		tables = page.extract_tables({
			"vertical_strategy": "text", 
		    "horizontal_strategy": "lines",
		    "text_tolerance": 10,
		    "min_words_vertical": 2,
		    # "explicit_horizontal_lines": rects_to_edges(page.rects)
		    "snap_tolerance": 8,
		    # "edge_min_length": 10
		    
		}) 

		# page.to_image(resolution=150).draw_rects(page.extract_words).save("./deb.png", format="PNG")

		print(tables)
		for table in tables:
			df=pd.DataFrame(table)
			df = df.replace('\n','', regex=True)
			df.to_csv(output_txt, index=True, header=False)
		

		