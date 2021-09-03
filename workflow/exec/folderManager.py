from pathlib import Path 
import os


# Folder Manager
# Add and remove folders


def create_TMP(batch_name,name):

	current = Path.cwd()
	folder = current/"tmp"/batch_name/name 
	if not Path(folder).exists():
		Path(folder).mkdir()


def create_PAGES_TMP(batch_name,name):

	current = Path.cwd()
	folder = current/"tmp"/batch_name/name/"pages"
	if not Path(folder).exists():
		Path(folder).mkdir()


def create_REG_TMP(batch_name,name):

	current = Path.cwd()
	folder = current/"tmp"/batch_name/name/"regions"
	if not Path(folder).exists():
		Path(folder).mkdir()


def create_RESULT(batch_name,name): 

	previous = Path.cwd().parents[0]
	folder = previous/"results"/batch_name
	if not Path(folder).exists():
		Path(folder).mkdir()



def create_RESULT_B(name): 

	previous = Path.cwd().parents[0]
	folder = previous/"results"/name
	if not Path(folder).exists():
		Path(folder).mkdir()


def create_TMP_B(name):

	current = Path.cwd()
	folder = current/"tmp"/name 
	if not Path(folder).exists():
		Path(folder).mkdir()


def delete_TMP(batch_name,name):

	current = Path.cwd()
	folder = current/"tmp"/batch_name/name
	for f in folder.glob(".JSON"):
		f.unlink()
	folder.rmdir()


def delete_REG_TMP(batch_name,name):

	current = Path.cwd()
	folder = current/"tmp"/batch_name/name/"regions"
	for f in folder.glob("*.JSON"):
		f.unlink()
	folder.rmdir()


def delete_IMG_TMP(batch_name,name):

	current = Path.cwd()
	folder = current/"tmp"/batch_name/name/"pages"
	for f in folder.glob("*.tiff"):
		f.unlink()

	for h in folder.glob("*.hocr"):
		h.unlink()
	
	folder.rmdir()


