import xml.etree.ElementTree as ET


def change_hocr(path,lista):
	tree = ET.parse(path)

	root = tree.getroot()

	for elem in lista:
		for delem in root.iter('span'):
			if delem.get('id').find("line") != -1 and delem.get('id') == elem['id']:
				for i, word in enumerate(list(delem)):
						word.text = elem['text'][i]
						old_conf = word.attrib['title']
						new_conf = old_conf.replace(old_conf.split(";")[1].split(" ")[2],str(elem['word_conf'][i]))
						word.set('title',new_conf)

	tree.write(path)
