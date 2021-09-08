import warnings
from PIL import Image
import cv2
import tesserocr as tr
from pathlib import Path
import json

warnings.simplefilter("ignore", Image.DecompressionBombWarning)

TESSDATA_PATH_BEST = Path.cwd()/'tessdata_best'
TESSDATA_PATH_FAST = Path.cwd()/'tessdata_fast'

def define_regions(image,langs):

	regions = []
	
	img = Image.open(image)

	lang = "+".join(langs)
	
	with tr.PyTessBaseAPI(path=str(TESSDATA_PATH_FAST), lang=lang) as api:
		api.SetImage(img)
		hocr_file = api.GetHOCRText(0)
		boxes = api.GetComponentImages(tr.RIL.TEXTLINE,True)		

		i = 1
		for (_1,box,_2,_3) in boxes:
			x,y,w,h = box['x'],box['y'],box['w'],box['h']
			region = {}
			region['id'] = "line_1_" + str(i)
			region['bbox'] = [x,y,x+w,y+h]
			region['coords'] = [x,y,w,h]
			region['filename'] = ""
			region['text'] = ""
			region['word_conf'] = 0 
			region['hocr_path'] = ""
			i+=1
			regions.append(region)

	return hocr_file, regions


def get_coords(regions):

	coords=[]
	for i in range(len(regions)):
		coords.append(regions[i]['coords'])
	return coords	


def crop(coords,image):

	img = cv2.imread(image)
	x,y,w,h= int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3]) 
	crop_img = img[y:y+h,x:x+w].copy()
	crop_img = cv2.copyMakeBorder(crop_img,50,50,50,50,cv2.BORDER_CONSTANT,value=[255,255,255])

	return crop_img



def save(tmpPathPages, tmpPathRegions, lang, tmp):
	if (tmpPathRegions/"regions.json").exists():
		return
	blocks = []
	for page_image in tmpPathPages.glob("page_*.tiff"):
		hocr_filename = tmpPathPages/(page_image.stem+".hocr")
		hocr_file, regions = define_regions(page_image, lang)
		block = {}
		block["image"] = page_image.name
		block["regions"] = regions
		blocks.append(block)
		hocr_filename.write_text(hocr_file)
		
		for i, region in enumerate(regions):
			filename = tmpPathRegions/(page_image.stem+'_%s.tiff'%(i+1))
			region["filename"] = str(filename)
			region["hocr_path"] = str(hocr_filename)
			result = crop(region["coords"], str(page_image))
			cv2.imwrite(str(filename),result)
	(tmpPathRegions/"regions.json").write_text(json.dumps(blocks))
