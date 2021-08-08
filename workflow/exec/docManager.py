import json
from pathlib import Path
import shutil
from PIL import Image
from PyPDF2 import PdfFileReader

def write_name(batch_name,file,pdf):				#file = /home/App/docs/S-1911-0009-0009-00001 UC.tiff
	if check_name(batch_name,file) == False:
		doc = make_doc(file,pdf)
		name = str(Path.cwd()/"tmp"/batch_name/doc['name'])+".JSON"
		update_data(name,doc)


def check_name(batch_name,file):
	filename = str(file.parts[-1]) + ".JSON"	#filename = S-1911-0009-0009-00001 UC.tiff.JSON
	path = Path.cwd()/"tmp"/batch_name/filename
	return path.exists()


def write_process(batch_name):
	process = make_process(batch_name)
	path = str(Path.cwd()/"tmp"/batch_name)+".JSON"
	update_data(path,process)


def make_doc(path,pdf):
	pages_left = 0

	if (pdf):
		pdf_path = open(path,'rb')
		pdf_reader = PdfFileReader(pdf_path)
		pages_left = pdf_reader.getNumPages()
	else:
		img = Image.open(path)
		pages_left = img.n_frames

	file = {}
	doc={}
	doc['split'] = pages_left
	doc['preprocess'] = pages_left
	doc['segment'] = pages_left
	doc['ocr'] = pages_left
	doc['compare'] = 1
	doc['merge'] = 1
	file['name'] = path.parts[-1]
	file['path'] = str(path)
	file['status'] = doc

	return file


def make_process(batch_name):

	process={}
	process['name'] = str(batch_name)
	process['files'] = []

	return process

def delete_process(batch_name):
	filename = str(Path.cwd()/"tmp"/batch_name) + ".JSON"
	Path(filename).unlink()

def add_file(batch_name,file):
	path = str(Path.cwd()/"tmp"/batch_name) +".JSON"
	data = get_data(path)
	data['files'].append(str(file))
	update_data(path,data)


def get_files(batch_name):
	path = str(Path.cwd()/"tmp"/batch_name) +".JSON"
	data =get_data(path)
	return data['files']


def update_field(batch_name,name,field,value):
	path = str(Path.cwd()/"tmp"/batch_name/name)+".JSON"
	data = get_data(path)
	data['status'][field] = value
	update_data(path,data)


def get_field(batch_name,name,field):
	path = str(Path.cwd()/"tmp"/batch_name/name)+".JSON"
	data = get_data(path)
	return data['status'][field]


def delete_data(batch_name,name):
	filename = str(Path.cwd()/"tmp"/batch_name/name) + ".JSON"
	Path(filename).unlink()


def update_data(name,data):
	with open(name,'w') as file:
		json.dump(data,file)


def get_data(name):
	with Path(name).open() as file:
		data = json.load(file)
		return data


def delete_regions(batch_name,name):
	path = Path.cwd()/"tmp"/batch_name/name/"regions"
	for elem in path.glob("*.tiff"):
		elem.unlink()



def parse_langs(langs):
	result = ""
	if isinstance(langs,tuple):
		for i in range(len(langs)):
			if i == 0:
				result = langs[i]
			else:
				result = result + "+" + langs[i]
	else:
		result = langs

	return result



