import tesserocr as tr
from PIL import Image
from pathlib import Path
import json 

TESSDATA_PATH = str(Path.cwd().parents[0]/'tessdata')

def ocr(tmpPathRegions,langs):
	regions = json.loads((tmpPathRegions/"regions.json").read_text())
	lang = "+".join(langs)

	for page in regions:
		for page_region in page["regions"]:
			region_image = Image.open(page_region["filename"])
			with tr.PyTessBaseAPI(path=TESSDATA_PATH, lang=lang, psm=tr.PSM.SINGLE_LINE) as api:
				api.SetImage(region_image)
				page_region["text"] = api.GetUTF8Text().replace("\n","").split()
				page_region["word_conf"] = api.AllWordConfidences()

	(tmpPathRegions/"regions.json").write_text(json.dumps(regions))
	
