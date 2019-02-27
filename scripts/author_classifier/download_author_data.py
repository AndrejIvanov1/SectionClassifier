"""
Usage:
	process_authors.py --target_file <target_file> --output_file <output_file>

Options:
	--target_file <target_file> File to process
	--output_file <output_file> Where to save the file with the abstracts
"""

"""
	Input: a file with author ids and pmc ids

	Output: the input file augmented with the actual abstract texts (downloaded from pmc) 
""" 

from docopt import docopt
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

s = requests.Session()
retries = Retry(total=5, backoff_factor=1)
s.mount('https://', HTTPAdapter(max_retries=retries))

min_abstract_length = 225

def not_valid_abstract(abstract):
	#print(len(abstract), abstract)
	return len(abstract) < min_abstract_length


def is_list_of_names(text):
	words = text.replace('\n', ' ').split()

	if len(words) == 1:
		return False 

	uppercase_words = float(len([w for w in words if w[0].isupper()]))

	if uppercase_words / len(words) > 0.7:
		#print("LIST OF NAMES: ", text)
		return True


def find_abstract(text):
	""" 
		The format of the text files is not consistent.
		Sometimes the abstract is the 3rd last paragraph, sometimes the 4th last.
	"""
	left = max(-6, -len(text))
	right = -2

	for i in range(left, right):
		#print(i, text[i])
		if "<?xml" in text[i] or \
		   "author information:" in text[i].lower() or \
		   "collaborators:" in text[i].lower() or \
		   "copyright: " in text[i].lower() or \
		   "Comment on" in text[i] or \
		   "Comment in" in text[i] or \
		   u"\xc2" in text[i] or \
		   is_list_of_names(text[i]):
			text[i] = ''

	return max(text[left:right], key=len)

def download_abstract(pm_id):		
	url = 'https://www.ncbi.nlm.nih.gov/pubmed/{}?report=abstract&format=text'.format(pm_id)
	
	r = s.get(url)
	text = r.content.decode('utf8')
	text = text.split('\n\n')

	abstract = find_abstract(text)
	abstract = abstract.replace('\n', ' ')

	return abstract

def add_abstracts(df, skip_until=9419):
	for index, row in df.iterrows():
		if index < skip_until:
			continue

		# If we already have an abstract, but it's invalid
		if df.loc[index].notna()['abstract'] and not_valid_abstract(df.loc[index]['abstract']):
			df.loc[index, 'abstract'] = np.NaN
		
		# If we have a valid abstract, continue
		if df.loc[index].notna()['abstract']:
			continue

		# Download and save abstract if we don't have it yet
		print("Index: {}, pm_id: {}".format(index, row['pm_id']))
		abstract = download_abstract(row['pm_id'])
		df.loc[index, 'abstract'] = abstract


if __name__ == "__main__":
	arguments = docopt(__doc__)
	filepath = arguments["<target_file>"]
	output_path = arguments["<output_file>"]
	
	df = pd.read_csv(filepath)
	#df['abstract'] = df['abstract'].apply(lambda abstract: abstract.replace('\n', ' ') if not pd.isnull(abstract) else abstract)
	try:
		add_abstracts(df)
	except Exception as e: 
		print(e)
	finally:
		print(df)
		df.to_csv(output_path, encoding='utf-8', index=False)

	#print(download_abstract('24711643'))