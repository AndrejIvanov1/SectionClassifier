from lxml import etree


class SectionParser:
    def __init__(self, xml_content):
        self.ET = etree.fromstring(xml_content)

    # <front>
    # .....
    # <abstract>
    def parse_abstract(self):
        res = {}
        for section in self.abstract_sections():
            title = self.format_title(section)

            if title is None:
                continue

            paragraphs = section.findall(".//p")

            res[title] = ' '.join([''.join(p.itertext()) for p in paragraphs]).replace('\n', ' ')

        return res

    def parse_body(self):
        res = {}
        for section in self.body_sections():
            title = self.format_title(section)

            if title is None:
                continue

            paragraphs = section.findall(".//p")

            res[title] = ' '.join([''.join(p.itertext()) for p in paragraphs]).replace('\n', ' ')

        return res

    def format_title(self, section):
        title = section.find("title").text
        if title is not None:
            title = title.replace('?', '').  \
                          replace('/', ' '). \
                          replace('\n', ''). \
                          replace('\"', ''). \
                          strip()

        if title == '':
            return None
        else:
            return title

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