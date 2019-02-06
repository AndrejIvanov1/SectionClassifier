"""
Usage:
    pmc_download.py --data_dir <data_dir> [--restore]

Options
    --data_dir <data_dir>
    --restore
"""
from urllib.request import urlretrieve
from ftplib import FTP
from docopt import docopt
import os
import tempfile
import tarfile
import time


from section_parser import SectionParser
from dataset_store import DatasetSaver

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
    Downloads all articles from the list, parses the sections and
    saves them under /data/body and /data/abstract
"""
def download_articles(max_number=100000, restore=False):

    if restore:
        skip_until = last_downloaded_file() + 1

    with open(local_list_path, 'r') as f:
        for index, line in enumerate(f):
            try:
                if index == 0:
                    continue
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

                xml_content = download_single_article(os.path.join(ftp_base_url, article_id))

                if xml_content is not None:
                    save_sections(xml_content)

                last_downloaded_file_is(index)

                #print("Time: ", time.time() - start_time)
            except Exception as e:
                print(e)
                with open("errors.txt", "a+", encoding='UTF-8') as err:
                    err.write("Error parsing # {} \n".format(index))


"""
    Input: xml_content - XML content of an article as a string

    Parses the sections from the xml and saves them in the 
    appropriate datasets.
"""
def save_sections(xml_content):
    parser = SectionParser(xml_content)
    abstract_sections = parser.parse_abstract()
    body_sections = parser.parse_body()

    ds = DatasetSaver(local_data_dir)
    ds.save_abstract(abstract_sections)
    ds.save_body(body_sections)



"""
    Input: url - link of an article on the FTP server

    Returns: None, if article is not found
             XML of article as string, if article is found
"""
def download_single_article(url):
    temp_file = 'tmpehotsd4z.tar.gz'

    print("Downloading {} into {}".format(url, temp_file))
    try:
        
        urlretrieve(url, temp_file)

        tar = tarfile.open(temp_file)
        for member in tar.getmembers():
            if member.name.endswith('xml'):
                print("XML file found: " + member.name)
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


def remove_html_markup(xml_content):
    html_mu = ['italic', 'i', 'b', 'bold', 'strong', 'em', 'small', 'mark', 'del', 'ins', 'sub', 'sup']

    for mu in html_mu:
        xml_content = xml_content.replace('<{}>'.format(mu), '')
        xml_content = xml_content.replace('</{}>'.format(mu), '')

    return xml_content


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
    print("arguments: ", arguments)
    restore = arguments['--restore']
    local_data_dir = arguments["--data_dir"]
    local_list_path = os.path.join(local_data_dir, files_list_name)

    if not os.path.exists(local_list_path):
        download_files_list()

    download_articles(max_number=1000000, restore=restore)