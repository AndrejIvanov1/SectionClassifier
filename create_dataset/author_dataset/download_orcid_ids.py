"""
Usage:
	download_orcid_ids.py --target_file <target_file> --output_file <output_file>

Options:
	--target_file <target_file> File to process
	--output_file <output_file> Where to save the file with the orcid ids
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
MAX_PUBMED_ID = int(25 * 1e6)
MAX_PMC_ID = 6411461

def pmc_url(pmc_id):
	return 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={}&retmode=xml'.format(pmc_id)

def pubmed_url(pubmed_id):
	url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={}&retmode=xml'.format(pubmed_id)

def download_article(id):		
	url = pmc_url(id)

	r = s.get(url)
	xml_content = r.content

	if 'orchid' in xml_content:
		print(xml_content)

	#text = r.content.decode('utf8')
	#text = text.split('\n\n')

	return 1

def add_orcid_ids(df, skip_until=MAX_PUBMED_ID):
	"""
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
		df.loc[index, 'abstract'] = abstract"""

	for id in reversed(range(MAX_PMC_ID)):
		if skip_until < id:
			continue

		print("Downloading: {}".format(id))
		xml_content = download_article(id)


if __name__ == "__main__":
	arguments = docopt(__doc__)
	filepath = arguments["<target_file>"]
	output_path = arguments["<output_file>"]
	
	df = pd.read_csv(filepath)
	try:
		add_orcid_ids(df)
	except Exception as e: 
		print(e)
	finally:
		print(df)
		df.to_csv(output_path, encoding='utf-8', index=False)

	#print(download_abstract('24711643'))