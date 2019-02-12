"""
Usage:
	biorelate_data_convert.py --input_dir <input_dir> --output_file <output_file>

Options:
	--input_dir <input_dir> Path to the input file
	--output_file <output_file> Path to output file
"""

import os
import json
import sys
sys.path.append('../create_dataset')
from titles import format_title
from convert_data_format import _save_dataset
from load_data import to_numeric_label
from fasttext_test import plot_class_distribution
from docopt import docopt

def read_articles(path):
	articles = []
	with open(path, 'r', encoding='UTF-8') as f:
		for index, line in enumerate(f):
			if index % 2 == 1:
				articles.append(line)

	return articles


def extract_section_text(section):
	name = section["name"]
	text = section["raw"].replace('\n', ' ').strip() + '\n'

	return name, text
	


def extract_sections(article_json):
	article_dict = json.loads(article_json)
	sections = article_dict["sections"]

	labeled_sections = [extract_section_text(section) for section in sections] 
	labeled_sections = [(format_title(pair[0], verbose=False), pair[1]) for pair in labeled_sections]
	labeled_sections = list(filter(lambda pair: pair[0] != 'Other' and pair[0] != 'Results', labeled_sections))
	
	#print(labeled_sections)
	return labeled_sections

if __name__ == "__main__":
	arguments = docopt(__doc__)
	input_path = arguments["<input_dir>"]
	output_path = arguments["<output_file>"]

	for filename in os.listdir(input_path):
		fullpath = os.path.join(input_path, filename)
		articles = read_articles(fullpath)

		labels = []
		data = []
		for article in articles:
			parsed_sections = extract_sections(article)
			if not parsed_sections:
				continue
			
			titles, texts = zip(*parsed_sections)
			titles = [to_numeric_label(title) for title in titles]

			labels.extend(titles)
			data.extend(texts)
		
		#plot_class_distribution(labels, title='Test class distribution')
		_save_dataset(data, labels, output_path)