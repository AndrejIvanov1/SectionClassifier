"""
Usage:
	process_authors.py --target_file <target_file> --output_file <output_file>

Options:
	--target_file <target_file> File to process
	--output_file <output_file> Where to save the file with the abstracts
"""

from docopt import docopt
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import matplotlib.pyplot as plt

s = requests.Session()
retries = Retry(total=5, backoff_factor=1)
s.mount('https://', HTTPAdapter(max_retries=retries))

def download_abstract(pm_id):		
	url = 'https://www.ncbi.nlm.nih.gov/pubmed/{}?report=abstract&format=text'.format(pm_id)
	
	r = s.get(url)
	text = r.content
	abstract = text.split('\n\n')[-3]

	return abstract

def add_abstracts(df):
	for index, row in df.iterrows():
		print("Index: {}, pm_id: {}".format(index, row['pm_id']))
		abstract = download_abstract(row['pm_id'])
		df.loc[index, 'abstract'] = abstract


if __name__ == "__main__":
	arguments = docopt(__doc__)
	filepath = arguments["<target_file>"]
	output_path = arguments["<output_file>"]
	
	df = pd.read_csv(filepath)
	
	try:
		add_abstracts(df)
	except:
		#print("Here")
		df.to_csv(output_path)
		df['abstract']

	df.to_csv(output_path)
	#print(download_abstract('22644237'))