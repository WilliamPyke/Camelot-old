from PyPDF2 import PdfWriter, PdfReader
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdf2image import convert_from_path

file_path = os.path.dirname(os.path.abspath(__file__))

config = open(file_path + '/config.txt', 'r')
configLines = config.readlines()
values = configLines[0].split()
fullname = configLines[1].strip()
date = configLines[2].strip()
values = tuple(map(int, values))

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(values[0], values[1], fullname)
can.drawString(values[2], values[3], date)
can.drawImage(file_path + "/signature.png", 125,87, width=120,height=40,mask=(0,0,0,0,0,0))
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfReader(packet)
# read your existing PDF
existing_pdf = PdfReader(open(file_path + "/PlagForm.pdf", "rb"))
output = PdfWriter()

# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
# finally, write "output" to a real file
output_stream = open(file_path + "/out.pdf", "wb")
output.write(output_stream)
output_stream.close()

pages = convert_from_path(file_path + "/out.pdf", 500)
for page in pages:
    page.save(file_path + '/out.png', 'PNG')