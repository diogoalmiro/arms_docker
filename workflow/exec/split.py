
#!/usr/bin/env python3

# Splits TIFF file into its different pages 
# Input: name of the file to be splitted (must be TIFF)
# Output: page_n.tiff (where n corresponds to the number of the page).

from PIL import Image
from pathlib import Path
import folderManager
import docManager

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

