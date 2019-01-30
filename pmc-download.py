from urllib.request import urlretrieve
from ftplib import FTP
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
local_list_path = os.path.join("data", files_list_name)
max_size_mgbs = 1000


"""
    Downloads a list of papers we can download from PMC.
    Stores it in ./data/oa_comm_use_file_list.txt
"""
def download_files_list():
    if not os.path.exists("data"):
        os.makedirs("data")

    urlretrieve(os.path.join(ftp_base_url, files_list_name), local_list_path)

def file_too_large(article_id):
    ftp = FTP(ftp_connection)
    ftp.login() 
    ftp.cwd('/pub/pmc')
    file_size_mgbs = ftp.size(article_id) / 1000000.0

    return file_size_mgbs > max_size_mgbs


"""
    Downloads all articles from the list, parses the sections and
    saves them under /data/body and /data/abstract
"""
def download_articles(max_number=1, skip_until=-1):

    with open(local_list_path, 'r') as f:
        for index, line in enumerate(f):
            try:
                if index == 0:
                    continue
                if index == max_number + 1:
                    break
                if index < skip_until:
                    continue

                print("ARTICLE # {} ------------------------------".format(index))
                article_id = line.rstrip().split("\t")[0]

                if (file_too_large(article_id)):
                    print("File too large: {}Mb".format(file_size_mgbs))
                    continue

                xml_content = download_single_article(os.path.join(ftp_base_url, article_id))

                if xml_content is not None:
                    save_sections(xml_content)
            except Exception as e:
                with open("errors.txt", "a+", encoding='UTF-8') as err:
                    err.write("Error parsing # {} \n".format(index))


def save_sections(xml_content):
    parser = SectionParser(xml_content)
    abstract_sections = parser.parse_abstract()
    body_sections = parser.parse_body()

    ds = DatasetSaver("data")
    ds.save_abstract(abstract_sections)
    ds.save_body(body_sections)


def download_single_article(url):
    temp_file = 'tmpehotsd4z.tar.gz'

    print("Downloading {} into {}".format(url, temp_file))
    try:
        
        urlretrieve(url, temp_file)

        # search for an xml file in the tar's files
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


if __name__ == "__main__":
    if not os.path.exists(local_list_path):
        download_files_list()

    download_articles(max_number=1000000, skip_until=51568)

