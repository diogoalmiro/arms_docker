#!/usr/bin/env python3
import split
import preprocess
import segment
import ocr
import compare
import merge
import sys
from pathlib import Path
import click
import time
import tempfile

def process(inputFile, outputFile, languages, keepTMP, doPreprocess, doComparisson ):
	fullname = inputFile.name
	name = inputFile.stem
	ext = inputFile.suffix.lower()

	tmpPath = Path(tempfile.gettempdir(), name)
	tmpPathPages = Path(tmpPath, 'pages')
	tmpPathRegions = Path(tmpPath, 'regions')

	tmpPathPages.mkdir(parents=True, exist_ok=True)
	tmpPathRegions.mkdir(parents=True, exist_ok=True)

	start = time.time();
	print("Splitting %s - "%name, end='')
	if ext == '.pdf':
		split.split_pages_pdf(inputFile, tmpPathPages)
	else:
		split.split_pages(inputFile, tmpPathPages)
	print("done (%s)"%(time.time() - start))
	print("Preprocessing %s - "%name, end='')
	preprocess.pre_process(inputFile, languages, doPreprocess, tmpPath)
	print("done (%s)"%(time.time() - start))
	print("Segmenting %s - "%name, end="")
	segment.save(tmpPathPages, tmpPathRegions, languages, keepTMP)
	print("done (%s)"%(time.time() - start))
	if doComparisson:
		print("OCRing %s - "%name, end="")
		ocr.ocr(tmpPathRegions, languages)
		print("done (%s)"%(time.time() - start))
		print("Comparing %s - "%name, end="")
		compare.modify(tmpPathPages, tmpPathRegions, keepTMP)
		print("done (%s)"%(time.time() - start))
	print("Merging %s - "%name, end="")
	merge.merge(tmpPathPages, outputFile, keepTMP)
	print("done (%s)"%(time.time() - start))
	
	if not keepTMP:
		for tmp in tmpPath.glob('**/*'):
			tmp.unlink()


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--comp/--no-comp',is_flag=True,help="Line segmentation comparison", default=True,show_default=True)
@click.option('--prep/--no-prep',is_flag=True,help="Additional prep-processing", default=False,show_default=True)
@click.option('--lang', multiple=True, show_default=True, default=['eng'],help="Use these languages to OCR.")
@click.option('--force',is_flag=True,help="Force OCR on files already processed", default=False,show_default=True)
@click.option('--tmp', is_flag=True ,help="Keep tmp files. WARNING: It requires more free disk space", default=False, show_default=True)
def main(path,lang,tmp,prep,comp,force):
	path = Path(path)
	if path.is_file():
		files = [path]
	elif path.is_dir():
		files = [ f for f in path.iterdir() if f.is_file() ]
	else:
		raise Exception("Path argument is not a valid folder or file")
	
	for file in files:
		fullname = file.name
		name = file.stem
		ext = file.suffix.lower()
		# Ignore files generated by us
		if ext == '.pdf' and '-ocr' in fullname:
			print("Ignoring %s"%file, file=sys.stderr)
			continue
		# Ignore unhandled extensions
		if ext != '.pdf' and ext != '.tiff' and ext != '.tif':
			print("Ignoring %s"%file, file=sys.stderr)
			continue
		
		# Check if we generated a -ocr.pdf file already
		processed = Path(file.parent,"%s-ocr.pdf"%name )
		if processed.exists():
			if force:
				processed.unlink()
			else:
				print("Ignoring %s"%file, file=sys.stderr)
				print("Use --force to restart OCR on %s"%file, file=sys.stderr)
				continue
		
		process(file, processed, lang, tmp, prep, comp)
				
	
if __name__ == "__main__":
	try:
		main()
		exit(0)
	except Exception as e:
		print(e)
		exit(1)
