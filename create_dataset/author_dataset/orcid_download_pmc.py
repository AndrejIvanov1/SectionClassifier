"""
Usage:
    orcid_download_pmc.py --target_file <target_file> --output_file <output_file> --list_file <list_file>

Options:
    --target_file <target_file> File to process
    --output_file <output_file> Where to save the file with the orcid ids
    --list_file <list_file> Where to find/download list of commercial use pmc files
"""
import sys

if sys.version_info[0] < 3:
    from urllib import urlretrieve
else:
    from urllib.request import urlretrieve
import io
from ftplib import FTP
from docopt import docopt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tempfile
import tarfile
import time

from orcid_parser import OrcidParser

ftp_connection = 'ftp.ncbi.nlm.nih.gov'
ftp_base_url = 'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/'
files_list_name = 'oa_comm_use_file_list.txt'
files_list_url = ftp_base_url + files_list_name
local_data_dir = ""
local_list_path = ""
MAX_SIZE_MGBS = 1000
BYTES_IN_MEGABYTE = 1000000.0

"""
    Downloads a list of papers we can download from PMC.
    Stores it in ./data/oa_comm_use_file_list.txt
"""
def download_files_list():
    print("Local data dir: ", local_data_dir)
    if not os.path.exists(local_data_dir):
        os.makedirs(local_data_dir)

    urlretrieve(os.path.join(ftp_base_url, files_list_name), local_list_path)


"""
    Checks whether a file from the FTP server is too large to download
"""
def file_too_large(article_id):
    ftp = FTP(ftp_connection)
    ftp.login() 
    ftp.cwd('/pub/pmc')
    file_size_mgbs = ftp.size(article_id) / BYTES_IN_MEGABYTE

    return file_size_mgbs > MAX_SIZE_MGBS


"""
    fsdadfsa
"""
def add_orcid_ids(df, max_number=100000, restore=False):
    skip_until = 197
    if restore:
        skip_until = last_downloaded_file() + 1

    with open(local_list_path, 'r') as f:
        for index, line in reversed(list((enumerate(f)))):
            try:
                if index == max_number + 1:
                    break
                if index < skip_until:
                    continue

                start_time = time.time()
                print("ARTICLE # {} ------------------------------".format(index))
                article_id = line.rstrip().split("\t")[0]

                if (file_too_large(article_id)):
                    print("File too large: {}Mb".format(file_size_mgbs))
                    continue

                url = os.path.join(ftp_base_url, article_id)
                xml_content = download_single_article(url)

                if xml_content is not None:
                    labeled_authors = parse(xml_content)
                    print("Labeled authors: " , labeled_authors)
                    labeled_authors = [author_info + (url,) for author_info in labeled_authors]
                    df = augment_df(df, labeled_authors)
                
                print(df)
                last_downloaded_file_is(index)
            except Exception as e:
                print(e)
                with open("errors.txt", "a+") as err:
                    pass
                    #err.write("Error parsing # {} \n".format(index))


def augment_df(df, labeled_authors):
    for firstname, lastname, orcid, url in labeled_authors:
        if already_contains(df, orcid):
            df = update_author_entry(df, orcid, url)
        else: # first time we get this author
            df = create_author_entry(df, firstname, lastname, orcid, url)

    return df

def update_author_entry(df, orcid, url):
    author_row = df.loc[df['orcid'] == orcid]
    author_row['urls'].append(url)

    return df

def create_author_entry(df, firstname, lastname, orcid, url):
    new_row = pd.DataFrame([[firstname, lastname, orcid, [url]]], columns=list(df))
    df = df.append(new_row)

    return df

def already_contains(df, orcid): 
    return orcid in df.orcid.values
"""
    Input: xml_content - XML content of an article as a string

"""
def parse(xml_content):
    parser = OrcidParser(xml_content)
    labeled_authors = parser.parse_orcid_id()

    return labeled_authors
"""
    Input: url - link of an article on the FTP server

    Returns: None, if article is not found
             XML of article as string, if article is found
"""
def download_single_article(url):
    temp_file = 'tmpehotsd4z.tar.gz'

    #print("Downloading {} into {}".format(url, temp_file))
    try:
        
        urlretrieve(url, temp_file)

        tar = tarfile.open(temp_file)
        for member in tar.getmembers():
            if member.name.endswith('xml'):
                #print("XML file found: " + member.name)
                content = tar.extractfile(member).read().decode('ascii')
                return content

        print("Couldn't find an xml file for " + url)
        return None
    except Exception as e:
        print(e)
        return None
    finally:
        pass
        # os.remove(temp_file)


def last_downloaded_file_is(index):
    with open("last_index.txt", 'w') as f:
        f.write(str(index))

def last_downloaded_file():
    try: 
        with open("last_index.txt", 'r') as f:
            return int(f.read().strip())
    except Exception as e:
        print(e)
        return -1  

if __name__ == "__main__":
    arguments = docopt(__doc__)
    filepath = arguments["--target_file"]
    output_path = arguments["--output_file"]
    local_list_path = arguments["--list_file"]

    local_list_path = os.path.join(local_list_path, files_list_name)
    if not os.path.exists(local_list_path):
        download_files_list()
    
    df = pd.read_csv(filepath)
    try:
        add_orcid_ids(df)
    except Exception as e: 
        print(e)
    finally:
        print(df)
        df.to_csv(output_path, encoding='utf-8', index=False)