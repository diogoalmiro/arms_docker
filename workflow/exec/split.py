
#!/usr/bin/env python3

# Splits TIFF file into its different pages 
# Input: name of the file to be splitted (must be TIFF)
# Output: page_n.tiff (where n corresponds to the number of the page).
import warnings
from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path
from pdf2image.generators import counter_generator

warnings.simplefilter("ignore", Image.DecompressionBombWarning)

def split_pages(file,pages_path):
	img = Image.open(file)
	for i in range(img.n_frames):
		page_path = pages_path/("page_%04d.tiff"%i)
		if not page_path.exists():
			try:
				img.seek(i)
				img.save(page_path, compression="raw")
			except EOFError:
				break


def split_pages_pdf(file,pages_path):
	pdf_pages = convert_from_path(file, paths_only=True, fmt="tiff") #output_file option creates weird filenames (issue: https://github.com/Belval/pdf2image/issues/183)
	for i, pdf_page in enumerate(pdf_pages):
		Path(pdf_page).rename(pages_path/("page_%04d.tiff"%i))
	