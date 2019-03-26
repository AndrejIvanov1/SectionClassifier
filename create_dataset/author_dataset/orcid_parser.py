from lxml import etree
"""
    A class for parsing sections from the XML of an article
"""
class OrcidParser:
    def __init__(self, xml_content):
        self.ET = etree.fromstring(xml_content)

        """
        if 'orcid' in xml_content:
            print("Orcid found")
        else:
            print("No orcid")"""
            
    """
    <contrib-group>
        <contrib contrib-type="author" corresp="yes">
            <name>
                <surname>Raufman</surname>
                <given-names>Jean-Pierre</given-names>
            </name>
            <contrib-id contrib-id-type="orcid">http://orcid.org/0000-0002-6340-4382</contrib-id>
        </contrib>
    </contrib-group>
    """
    def parse_orcid(self, contributor):
        orcid_id = contributor.xpath('./contrib-id[@contrib-id-type="orcid"]')
        if orcid_id == []:
            return None

        return orcid_id[0].text

    def parse_first_name(self, contributor):
        first_name = contributor.xpath('./name/given-names')[0]

        return first_name.text

    def parse_last_name(self, contributor):
        last_name = contributor.xpath('./name/surname')[0]

        return last_name.text

    """
        Returns: list of tuples: (firstname, lastname, orcid)
    """
    def parse_orcid_id(self):
        contributors = self.ET.xpath("//contrib-group")[0]
        labeled_authors = []
        for contributor in contributors:
            orcid = self.parse_orcid(contributor)
            if orcid is None:
                continue

            first_name = self.parse_first_name(contributor)
            last_name = self.parse_last_name(contributor)

            labeled_authors.append((first_name, last_name, orcid))

        return labeled_authors


    def parse_pmc_id(self):
        pmc_id_field = self.ET.xpath("//article-id[@pub-id-type='pmc']")
        if not pmc_id_field:
            return None

        pmc_id = pmc_id_field[0]
        return pmc_id.text


if __name__ == "__main__":
    xml_content = ' <contrib-group> \
        <contrib contrib-type="author" corresp="yes"> \
            <name> \
                <surname>Raufman</surname> \
                <given-names>Jean-Pierre</given-names> \
            </name> \
            <contrib-id contrib-id-type="orcid">http://orcid.org/0000-0002-6340-4382</contrib-id> \
        </contrib> \
    </contrib-group>'
    parser = OrcidParser(xml_content)
    print(parser.parse_orcid_id())
