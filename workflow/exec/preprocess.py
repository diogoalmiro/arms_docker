import os 
from tesserocr import PyTessBaseAPI, RIL
from PIL import Image
from pathlib import Path
import cv2

TESSDATA_PATH_BEST = Path.cwd()/'tessdata_best'
TESSDATA_PATH_FAST = Path.cwd()/'tessdata_fast'

def pre(image,langs):
	lang = "+".join(langs)
	img = Image.open(image)

	with PyTessBaseAPI(path=str(TESSDATA_PATH_FAST), lang=lang) as api:
		api.SetImage(img)
		input_img = api.GetThresholdedImage()

	return input_img



def pre_process(tmpPathPages, tmpPathRegions, langs, prep):
	for page_image in tmpPathPages.glob("page_*.tiff"):
		dest = tmpPathRegions/page_image;
		if dest.exists():
			continue
		processed = pre(page_image, langs);
		if(prep):
			add_preprocess(page_image, dest)
		else:
			processed.save(dest)
		

def add_preprocess(img_path,img_name):
	image = cv2.imread(str(img_path))

	g = get_grayscale(image)
	rn = remove_noise(g)
	t = thresholding(rn)
	final = dilate(t)

	cv2.imwrite(str(img_name),final)


# get grayscale image
def get_grayscale(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return img
    
# noise removal
def remove_noise(image):
    img = cv2.medianBlur(image,5)
    return img
 
#thresholding
def thresholding(image):
    img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return img

#dilation
def dilate(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    img = cv2.dilate(image, kernel, iterations = 1)
    return img
   
