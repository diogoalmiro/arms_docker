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
import time


def to_do(file,lang,tmp,prep,comp,batch_name):
	n = file['name']
	status = file['status']
	path = file['path']

	if (status['split']):
		st2 = time.time()
		print(" ")
		print("Splitting %s"%n)
		folderManager.create_TMP(batch_name,n)
		folderManager.create_PAGES_TMP(batch_name,n)
		split.split_pages(Path(path),batch_name)
		print("%s splitted - %s"%(n,(time.time()-st2)))


	if (status['preprocess']):
		st3 = time.time()
		print(" ")
		print("Preprocessing %s"%n)
		folderManager.create_REG_TMP(batch_name,n)
		preprocess.pre_process(n,lang,prep,batch_name)
		print("%s preprocessed - %s"%(n,(time.time()-st3)))

	if (status['segment']):
		st4 = time.time()
		print(" ")
		print("Segmenting %s"%n)
		segment.save(n,lang,tmp,batch_name)
		print("%s segmented - %s"%(n,(time.time()-st4)))

	if (status['ocr'] and comp):
		st5 = time.time()
		print(" ")
		print("OCR %s"%n)
		ocr.ocr(n,lang,batch_name)
		print("%s OCR done - %s"%(n,(time.time()-st5)))

	if (status['compare'] and comp):
		st6 = time.time()
		print(" ")
		print("Comparing results of %s"%n)
		compare.modify(n,tmp,batch_name)
		docManager.update_field(batch_name,n,'compare',0)
		print("%s results compared - %s"%(n,(time.time()-st6)))

	if (status['merge']):
		st7 = time.time()
		print(" ")
		print("Merging %s"%n)
		folderManager.create_RESULT(batch_name,n)
		merge.merge(n,tmp,batch_name)
		docManager.update_field(batch_name,n,'merge',0)
		print("%s merged - %s"%(n,(time.time()-st7)))


	docManager.delete_data(batch_name,n)


def process(image,batch_name,lang,tmp,prep,comp):
	inputFile = Path(image)
	docManager.write_name(batch_name,inputFile)
	doc = docManager.get_data(str(Path.cwd()/"tmp"/batch_name/inputFile.parts[-1]) + '.JSON')
	to_do(doc,lang,tmp,prep,comp,batch_name)
	docManager.add_file(batch_name,inputFile)
	print("Done")


def exists(batch_name):
	if((Path.cwd()/"tmp"/(str(batch_name+".JSON"))).exists()):
		return True


def forcing(path):
	batch_name = str(path.parts[-1])
	process = Path.cwd()/"tmp"/batch_name
	if exists(batch_name):
		for file in process.glob("*.JSON"):
			Path(file).unlink()
		docManager.delete_process(batch_name)


@click.command()
@click.argument('file')
@click.option('--comp',is_flag=True,help="Line segmentation comparison", default=True,show_default=True)
@click.option('--prep',is_flag=True,help="Additional prep-processing", default=False,show_default=True)
@click.option('--lang',type=click.Choice(tesserocr.get_languages(str(Path.cwd().parents[0]/'tessdata'))[1], case_sensitive=False), multiple=True, show_default=True, default=('eng',),help="Available languages.")
@click.option('--force',is_flag=True,help="Start from the beggining", default=False,show_default=True)
@click.option('--tmp', is_flag=True ,help="Keep tmp files. WARNING: It requires more free disk space", default=False, show_default=True)
@click.option('--folder', is_flag=True ,help="Workflow is performed in all images from this folder", default=False, show_default=True)



def main(file,lang,tmp,folder,prep,comp,force):
	st1= time.time()
	files = []
	if (folder):
		
		path = Path(file)
		batch_name = str(path.parts[-1])
		
		if (force):
			forcing(path)
			folderManager.create_TMP_B(batch_name)
			folderManager.create_RESULT_B(batch_name)
			docManager.write_process(batch_name)
			
			for image in path.glob("*.tif"):
					image.rename(image.with_suffix(".tiff"))

			for image in path.glob("*.tiff"):
					process(image,batch_name,lang,tmp,prep,comp)
		
		else: 
			if exists(batch_name):
				
				print("{} already exists and the process will continue".format(batch_name))
				print("To start again, use --force ")
				files = docManager.get_files(batch_name)
				
				for image in path.glob("*.tif"):
					if str(image) not in files:
						image.rename(image.with_suffix(".tiff"))

				for image in path.glob("*.tiff"):
					if str(image) not in files:
						process(image,batch_name,lang,tmp,prep,comp)
			else: 
				
				folderManager.create_TMP_B(batch_name)
				folderManager.create_RESULT_B(batch_name)
				docManager.write_process(batch_name)
				
				for image in path.glob("*.tif"):
						image.rename(image.with_suffix(".tiff"))

				for image in path.glob("*.tiff"):
						process(image,batch_name,lang,tmp,prep,comp)

	else:
		path = Path(file)
		batch_name = str(path.parts[-1])

		if (force):
			forcing(path)
			folderManager.create_TMP_B(batch_name)
			folderManager.create_RESULT_B(batch_name)
			docManager.write_process(batch_name)
			process(path,batch_name,lang,tmp,prep,comp)

		else: 
			if exists(batch_name):
				print("{} already exists and the process will continue. To start again, use --force".format(batch_name))
				files = docManager.get_files(batch_name)
				if str(file not in files):
					process(file,batch_name,lang,tmp,prep,comp)
			else: 
				folderManager.create_TMP_B(batch_name)
				folderManager.create_RESULT_B(batch_name)
				docManager.write_process(batch_name)
				process(path,batch_name,lang,tmp,prep,comp)

	print("Process completed. To start again, use --force")

	

if __name__ == "__main__":
	main()
