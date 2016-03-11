import json
from bs4 import BeautifulSoup
import os
import sys
from clean_xml import *

def write_json(json_obj, filepath):
    """Take dict and write JSON and filepath, write JSON to file."""
    dirs, name = os.path.split(filepath)

    # Remove .xml and add .json to filename
    name_json = name[:-len('.xml')] + '.json'

    fp_json = os.path.join(dirs, name_json)
    with open(fp_json, 'w') as file_open:
        json.dump(json_obj, file_open)


def parser(soup):
	tei = soup.find('TEI.2')

	tei_header = tei.find('teiHeader')
	file_desc = tei_header.find('fileDesc')
	title_statement = file_desc.find('titleStmt')
	title = title_statement.find('title')
	author = title_statement.find('author')

	dict_object = {}
	dict_object['title'] = title.text
	dict_object['author'] = author.text

	# Parse body
	dict_text = {}
	text = tei.find('text')
	body = text.find('body')
	div1 = body.find('div1')
	type = div1.get('type')
	#print(type)
	dict_object['meta'] = type

	l = div1.find_all('l')
	#print(l)

	for number in range(len(l)):
		dict_text[number+1] = l[number].string

	dict_object['text'] = dict_text
	return dict_object


def main():
	filepath_xml = 'verg.g_lat.xml'
	xml_str = cleanup_file_perseus_xml(filepath_xml)
	soup = BeautifulSoup(xml_str, 'xml')
	
	dict_object = parser(soup)
	write_json(dict_object, filepath_xml)

if __name__ == '__main__':
	main()