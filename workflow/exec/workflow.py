#!/usr/bin/env python3
import split
import docManager
import preprocess
import segment
import ocr
import compare
import merge
import sys
from pathlib import Path
import click
import tesserocr
import datetime
import folderManager

def get_batches():
	batches = []
	path = Path.cwd()/"tmp"
	for batch in path.glob("*.JSON"):
		batches.append(str(batch.stem))

	return batches



def to_do(file,lang,tmp,prep,comp,batch_name):
	n = file['name']
	status = file['status']
	path = file['path']

	if (status['split']):
		print("Splitting %s"%n)
		folderManager.create_TMP(batch_name,n)
		folderManager.create_PAGES_TMP(batch_name,n)
		split.split_pages(Path(path),batch_name)
		print("%s splitted"%n)

	if (status['preprocess']):
		print("Preprocessing %s"%n)
		folderManager.create_REG_TMP(batch_name,n)
		preprocess.pre_process(n,lang,prep,batch_name)
		print("%s preprocessed"%n)

	if (status['segment']):
		print("Segmenting %s"%n)
		segment.save(n,lang,tmp,batch_name)
		print("%s segmented"%n)

	if (status['ocr'] and comp):
		print("OCR %s"%n)
		ocr.ocr(n,lang,batch_name)
		print("%s OCR done"%n)

	if (status['compare'] and comp):
		print("Comparing results of %s"%n)
		compare.modify(n,tmp,batch_name)
		docManager.update_field(batch_name,n,'compare',0)
		print("%s results compared"%n)

	if (status['merge']):
		print("Merging %s"%n)
		folderManager.create_RESULT(batch_name,n)
		merge.merge(n,tmp,batch_name)
		docManager.update_field(batch_name,n,'merge',0)
		print("%s merged"%n)


	docManager.delete_data(batch_name,n)


def process(image,batch_name,lang,tmp,prep,comp):
	inputFile = Path(image)
	docManager.write_name(batch_name,inputFile)
	doc = docManager.get_data(str(Path.cwd()/"tmp"/batch_name/inputFile.parts[-1]) + '.JSON')
	to_do(doc,lang,tmp,prep,comp,batch_name)
	docManager.add_file(batch_name,inputFile)
	print("Done")


@click.command()
@click.argument('file')
@click.option('--comp',is_flag=True,help="Disable line segmentation comparison", default=True,show_default=True)
@click.option('--prep',is_flag=True,help="Additional prep-processing", default=False,show_default=True)
@click.option('--lang',type=click.Choice(tesserocr.get_languages(str(Path.cwd().parents[0]/'tessdata'))[1], case_sensitive=False), multiple=True, show_default=True, default=('eng',),help="Available languages.")
@click.option('--proc',type=click.Choice(get_batches(), case_sensitive=False), multiple=True,help="Unfinished processes.")
@click.option('--tmp', is_flag=True ,help="Keep tmp files. WARNING: It requires more free disk space", default=False, show_default=True)
@click.option('--folder', is_flag=True ,help="Workflow is performed in all images from this folder", default=False, show_default=True)



def main(file,lang,tmp,folder,prep,comp,proc):
	files = []
	
	if (proc):
		batch_name = proc[0]
		files = docManager.get_files(batch_name)

	else:
		batch_name = "batch_" + str(datetime.datetime.now().timestamp())
		folderManager.create_TMP_B(batch_name)
		folderManager.create_RESULT_B(batch_name)
		docManager.write_process(batch_name)

	if (folder):
		path = Path(file)
		for image in path.glob("*.tif"):
			if str(image) not in files:
				image.rename(image.with_suffix(".tiff"))

		for image in path.glob("*.tiff"):
			if str(image) not in files:
				process(image,batch_name,lang,tmp,prep,comp)

	else:
		if image not in files:
			process(image,batch_name,lang,tmp,prep,comp)


	docManager.delete_process(batch_name)

if __name__ == "__main__":
	main()
