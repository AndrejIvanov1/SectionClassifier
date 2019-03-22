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

s = requests.Session()
retries = Retry(total=5, backoff_factor=1)
s.mount('https://', HTTPAdapter(max_retries=retries))

"""
	Input: firstname and lastname of author
	Output: NCBI eutils url to search pmc papers for the given author name
"""
def papers_for_author_url(firstname, lastname):
    url_whitespace = '%20' # url convention
    fullname = '{firstname} {lastname}'.format(firstname=firstname, lastname=lastname)
    fullname = fullname.replace(' ', url_whitespace)

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={}[AU]&retmax=50'.format(fullname)
    return url


"""
    Input: a pmc id
    Output: url to download the xml of the paper with that pmc id
"""
def pmc_url(pmc_id):
    return 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={}&retmode=xml'.format(pmc_id)


def download_paper(pmc_id, wait=0):
    time.sleep(wait*1000)       
    url = pmc_url(pmc_id)

    r = s.get(url)
    xml_content = r.content

    return xml_content
"""
    Input:  firstname, lastname, orcid of author
    Output: list of PMC ids of articles written by different authors
            with the same name
"""
def find_same_name_articles(firstname, lastname, orcid):
    url = papers_for_author_url(firstname, lastname)
    r = s.get(url)
    xml_content = r.content
    ids = parse_ids(xml_content)

    for pmc_id in ids:
        xml_content = download_paper(pmc_id, wait=0.00)
        parser = OrcidParser(xml_content)
        pmc_id = parser.parse_pmc_id()
        print(pmc_id)
        input()
        labeled_authors = parser.parse_orcid_id()

    return ids

if __name__ == "__main__":
    arguments = docopt(__doc__)
    filepath = arguments["--target_file"]

    #df = pd.read_csv(filepath)

    firstname, lastname, orcid = 'Kristin M.', 'Wall', 'http://orcid.org/0000-0001-8547-2004'
    find_same_name_articles(firstname, lastname, orcid)
    


    