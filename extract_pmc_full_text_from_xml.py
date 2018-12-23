#!/usr/bin/env python

import pubmed_parser as pp
import json
import sys
import codecs

#path_xml_input = str(sys.argv[1])
#path_json_data = str(sys.argv[2])
#path_json_para = str(sys.argv[2])


def extract_sections(xml_string):
    result = {}
    data_dict = pp.parse_pubmed_xml(xml_string)
    para_dict = pp.parse_pubmed_paragraph(xml_string)

    # result.insert(0,{
    #     "text"   : data_dict['abstract'],
    #     "section": "Abstract"
    # })
    #
    # result.insert(0,{
    #     "text": data_dict['full_title'],
    #     "section": "Title"
    # })


    # print('xxxx')
    # print(data_dict['full_title'])
    # print(json.dumps(data_dict['full_title']).strip('"'))
    result['abstract'] = json.dumps(data_dict['abstract'])
    result['title'] = json.dumps(data_dict['full_title'])


    current_section = None
    full_text = ''
    for section in para_dict:
        if not current_section == section['section']:
            current_section = section['section']
            full_text += current_section + '\n'
        full_text += section['text'] + '\n'

    result['full_text'] = json.dumps(full_text).strip('"')



    # return json.dumps(para_dict, sort_keys = False, indent = 4,ensure_ascii=False)
    # return json.dumps(result, sort_keys = False, indent = 4,ensure_ascii=False)
    return  result
