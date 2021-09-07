from pathlib import Path
import parser_r as pr
import parser_w as pw
import json
import shutil

def get_ocr(tmpPathRegions):
	return json.loads((tmpPathRegions/"regions.json").read_text())

def get_hocr(page):
	lines = []
	areas = pr.get_areas(page)
	for area in areas:
		line = pr.get_lines(page,area['id'])
		for element in line:
			lines.append(element)
	return lines


def compare(hocrPage, tmpPathPages, tmpPathRegions):
	aux = get_ocr(tmpPathRegions)
	d1 = get_hocr(hocrPage)
	new_d1 = []

	image = str(hocrPage.stem) + ".tiff"

	for page in aux:
		if page['image'] == image:
			d2 = page['regions']

	for i in d1:
		for h in d2:
			if i['bbox'] == h['bbox'] and (i['word_conf'] != h['word_conf']):
				
				best = [max(value) for value in zip(i['word_conf'],h['word_conf'])]
				for r in range(len(best)):
					if best[r] == h['word_conf'][r]:
						i['text'][r] = h['text'][r] 
						i['word_conf'][r] = h['word_conf'][r]

				new_d1.append(i)

			elif  i['bbox'] == h['bbox'] and (i['word_conf'] == h['word_conf']):

				new_d1.append(i)

	return new_d1


def modify(tmpPathPages, tmpPathRegions, tmp):
	for page in tmpPathPages.glob("*.hocr"):
		changes = compare(page, tmpPathPages, tmpPathRegions)
		pw.change_hocr(page,changes)

		if not tmp:
			for region in tmpPathRegions.glob("*.tiff")
				region.unlink()


					




