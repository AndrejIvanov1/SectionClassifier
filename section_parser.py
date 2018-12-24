from lxml import etree
from titles import format_title

class SectionParser:
    def __init__(self, xml_content):
        self.ET = etree.fromstring(xml_content)

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
        return self.ET.xpath("front//abstract/sec[title]")


if __name__ == "__main__":
    xml_content = open('article-long.nxml', 'r').read()
    parser = SectionParser(xml_content)
    parser.parse_abstract()
    body_sections = parser.parse_body()
    print(body_sections.keys())