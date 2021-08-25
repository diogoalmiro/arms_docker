
#!/usr/bin/env python3

# Splits TIFF file into its different pages 
# Input: name of the file to be splitted (must be TIFF)
# Output: page_n.tiff (where n corresponds to the number of the page).

import warnings
from PIL import Image
from pathlib import Path
import folderManager
import docManager
from pdf2image import convert_from_path

warnings.simplefilter("ignore", Image.DecompressionBombWarning)

def split_pages(file,batch_name):
	img_path = file
	name = file.parts[-1]
	pages_path = str(Path.cwd()/"tmp"/batch_name/name/"pages")
	img = Image.open(img_path)
	pages_left = docManager.get_field(batch_name,name,'split')

	for i in range(pages_left,-1,-1):
		try:
			img.seek(i-1)
			img.save(pages_path + "/page_%s.tiff" %i, compression="raw")
			docManager.update_field(batch_name,name,'split',(i-1))
		except EOFError:
			break


def split_pages_pdf(file,batch_name):
	name = file.parts[-1]
	pages_path = str(Path.cwd()/"tmp"/batch_name/name/"pages")
	pages_left = docManager.get_field(batch_name,name,'split')
	for page in range(1, pages_left+1, 10) : 
   		convert_from_path(file, dpi=200, first_page=page, last_page = min(page+10-1,pages_left))

	for i in range(pages_left,0,-1):
		try:
			pdf_file[i-1].save(pages_path + "/page_%s.tiff" %i, 'TIFF')
			docManager.update_field(batch_name,name,'split',(i-1))
		except EOFError:
			break		


