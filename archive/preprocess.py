from fpdf import FPDF

linePDF = FPDF()
linePDF.add_page(orientation='P', format='A4')
linePDF.set_fill_color(0,0,0)
linePDF.rect(34,275,156,0.5,'F')
linePDF.add_page()
linePDF.set_fill_color(0,0,0)
linePDF.rect(34,281.5,156,0.5,'F')

linePDF.output('component/line.pdf', 'F')


from PyPDF2 import PdfFileWriter, PdfFileReader

filename = "68_1308.pdf"
outputPDF = PdfFileWriter()
sourcePDF = PdfFileReader(open('./pdf/' + filename, "rb"))

# print how many pages sourcePDF has:
print (sourcePDF.numPages)
# print ("source pdf has " + sourcePDF.numPages.str + " pages.")

# # add page 1 from sourcePDF to outputPDF document, unchanged
# outputPDF.addPage(sourcePDF.getPage(0))

# # add page 2 from sourcePDF, but rotated clockwise 90 degrees
# outputPDF.addPage(sourcePDF.getPage(1))

# # add page 3 from sourcePDF, rotated the other way:
# outputPDF.addPage(sourcePDF.getPage(2).rotateCounterClockwise(90))
# # alt: outputPDF.addPage(sourcePDF.getPage(2).rotateClockwise(270))

# add page 4 from sourcePDF, but first add a watermark from another PDF:

linePDF = PdfFileReader(open("component/line.pdf", "rb"))

for pageNum in range(sourcePDF.numPages):
    if pageNum == 2:
        linePlace = linePDF.getPage(0)
    else :
        linePlace = linePDF.getPage(1)

    if pageNum >= 2:
        currentPage = sourcePDF.getPage(pageNum)
        currentPage.mergePage(linePlace)
        outputPDF.addPage(currentPage)

# encrypt your new PDF and add a password
# password = "secret"
# outputPDF.encrypt(password)

# finally, write "outputPDF" to document-outputPDF.pdf
outputPDFStream = open('./pdf/processed_' + filename, "wb")
outputPDF.write(outputPDFStream)

