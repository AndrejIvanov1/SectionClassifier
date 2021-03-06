from lxml import etree


"""
	Input: xml returned from the NCBI esearch api
	Output: list of ids returned by esearch 
"""
def parse_ids(xml_content):
	ET = etree.fromstring(xml_content)
	id_list = ET.xpath("//IdList")[0]
	ids = id_list.xpath("./Id")

	ids = [id_field.text for id_field in ids]

	return ids