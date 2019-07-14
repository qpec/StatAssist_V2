def add_highlights_to_pages(input_pdf_path, data, out_pdf_path, total_pages):
	print("Highlighter started...")
	output = PdfFileWriter()
	# read your existing PDF
	existing_pdf = PdfFileReader(file(input_pdf_path, "rb"))
	pages = []
	print("Input pdf: " + input_pdf_path)

	for i in range(0,total_pages+1):
		pages.append(existing_pdf.getPage(i))

	for word in data:
		color = data[word]["color"]
		cords = data[word]["cords"]
		page_num = data[word]["page"]

		packet = StringIO.StringIO()
		canvas = create_canvas(cords, color, packet)
		# merge changes with the old pdf
		# move to the beginning of the StringIO buffer
		packet.seek(0)
		new_pdf = PdfFileReader(packet)
		# add the "watermark" (which is the new pdf) on the existing page
		(pages[page_num]).mergePage(new_pdf.getPage(0))

	for page in pages:
		output.addPage(page)

	# finally, write "output" to a real file
	outputStream = file(out_pdf_path, "wb")
	output.write(outputStream)
	outputStream.close()


# creates and returns a new pdf
# pdf contains a box in the specified color, location and dimensions
def create_canvas(cords, color, packet):
	# create a new PDF with Reportlab
	c = Canvas(packet, pagesize=letter)
	#c.drawString(10, 100, "Hello world")
	cmyk_color = get_color_with_opacity(color, 40)	# 40% opacity

	c.setFillColor(cmyk_color)
	x1 = cords[0]
	y1 = cords[1]
	x2 = cords[2]
	y2 = cords[3]
	#rect arguments are(x,y,width,height)
	c.rect(x1,y1,x2-x1,y2-y1, fill=True, stroke=False)
	c.save()
	return c
