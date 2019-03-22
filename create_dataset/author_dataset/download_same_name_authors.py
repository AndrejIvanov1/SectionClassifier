"""
Usage:
    download_same_name_authors.py --target_file <target_file> 

Options:
    --target_file <target_file> File to process
"""
from docopt import docopt
import pandas as pd
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import time

from parser import parse_ids
from orcid_parser import OrcidParser
import df_utils as dfu

s = requests.Session()
retries = Retry(total=5, backoff_factor=1)
s.mount('https://', HTTPAdapter(max_retries=retries))

df = ''

"""
	Input: firstname and lastname of author
	Output: NCBI eutils url to search pmc papers for the given author name
"""
def papers_for_author_url(firstname, lastname):
    url_whitespace = '%20' # url convention
    fullname = '{firstname} {lastname}'.format(firstname=firstname, lastname=lastname)
    fullname = fullname.replace(' ', url_whitespace)

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={}[AU]&retmax=10'.format(fullname)
    return url


"""
    Input: a pmc id
    Output: url to download the xml of the paper with that pmc id
"""
def pmc_url(pmc_id):
    return 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={}&retmode=xml'.format(pmc_id)


def download_paper(pmc_id, wait=0):
    time.sleep(wait)       
    url = pmc_url(pmc_id)

    r = s.get(url)
    print(url)
    xml_content = r.content

    return xml_content
"""
    Input:  firstname, lastname, orcid of author
    Output: list of PMC ids of articles written by different authors
            with the same name
"""
def find_same_name_authors(firstname, lastname, orcid):
    global df

    url = papers_for_author_url(firstname, lastname)
    r = s.get(url)
    xml_content = r.content
    ids = parse_ids(xml_content)

    for pmc_id in ids:
        if dfu.has_pmc_id(df, pmc_id):
            continue

        xml_content = download_paper(pmc_id, wait=0.5)
        parser = OrcidParser(xml_content)
        pmc_id = parser.parse_pmc_id()
        
        labeled_authors = parser.parse_orcid_id()
        print("Labeled authors: ", labeled_authors)
        labeled_authors = [author_info + (pmc_id,) for author_info in labeled_authors]
        df = dfu.augment_df(df, labeled_authors)

    df.to_csv(filepath, encoding='utf-8', index=False)

    return ids

def add_authors(skip_until=0):
    for index, row in df.iterrows():
        if index < skip_until:
            continue

        print("Index: {}".format(index))
        find_same_name_authors(row['firstname'], row['lastname'], row['orcid'])

if __name__ == "__main__":
    arguments = docopt(__doc__)
    filepath = arguments["--target_file"]

    df = pd.read_csv(filepath)

    add_authors(skip_until=44)
    


    