from lxml import etree
"""
    A class for parsing sections from the XML of an article
"""
class OrcidParser:
    def __init__(self, xml_content):
        self.ET = etree.fromstring(xml_content)

    def parse_orcid_id(self):
        contrib_tag = self.ET.xpath("//contrib-id")
        print([t.text for t in contrib_tag])
    """
    # <front>
    # .....
    # <abstract>
    def parse_abstract(self):
        res = {}
        for section in self.abstract_sections():
            title = self.find_title(section)

            if title is None:
                continue

            title = format_title(title)

            paragraphs = section.findall(".//p")

            res[title] = ' '.join([''.join(p.itertext()) for p in paragraphs]).replace('\n', ' ')

        return res

    def parse_body(self):
        res = {}
        for section in self.body_sections():
            title = self.find_title(section)

            if title is None or title == '':
                continue

            title = format_title(title)

            if title == 'Other':
                continue

            paragraphs = section.findall(".//p")

            res[title] = ' '.join([''.join(p.itertext()) for p in paragraphs]).replace('\n', ' ')

        return res

    def find_title(self, section):
        return section.find("title").text

    def body_sections(self):
        return self.ET.xpath("body/sec[title]")

    def abstract_sections(self):
        return self.ET.xpath("front//abstract/sec[title]") """


if __name__ == "__main__":
    xml_content = open("example.xml", 'r').read().replace('&', '')
    parser = OrcidParser(xml_content)
    parser.parse_orcid_id()
    pass