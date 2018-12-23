from urllib.request import urlretrieve
import os
import tempfile
import tarfile
import time

from section_parser import SectionParser
from dataset_store import DatasetSaver

ftp_base_url = 'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/'
files_list_name = 'oa_comm_use_file_list.txt'
files_list_url = ftp_base_url + files_list_name
local_list_path = os.path.join("data", files_list_name)


def download_files_list():
    urlretrieve(os.path.join(ftp_base_url, files_list_name), local_list_path)


def download_articles(max_number=1, skip_until=-1):

    with open(local_list_path, 'r') as f:
        for index, line in enumerate(f):
            if index == 0:
                continue
            if index == max_number + 1:
                break
            if index < skip_until:
                continue

            print("ARTICLE # {} ------------------------------".format(index))

            article_id = line.rstrip().split("\t")[0]
            xml_content = download_single_article(os.path.join(ftp_base_url, article_id))

            if xml_content is not None:
                save_sections(xml_content)


def save_sections(xml_content):
    parser = SectionParser(xml_content)
    abstract_sections = parser.parse_abstract()
    body_sections = parser.parse_body()

    with open("sections.txt", 'a+', encoding='UTF-8') as f:
        f.write(','.join(body_sections.keys()) + '\n')

    # ds = DatasetSaver("data")
    # ds.save_abstract(abstract_sections)
    # ds.save_body(body_sections)

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

    download_articles(max_number=1000000, skip_until=293)

