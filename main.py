import json
import requests
import xml.etree.ElementTree as ET


def convert_to_xml(data_str):
    tree = ET.ElementTree(ET.fromstring(data_str))
    return tree


jsonList = []
with open('periodicals_translated_v2_tiny.jsonl', encoding="utf8") as f:
    for jsonObj in f:
        jsonDict = json.loads(jsonObj)
        jsonList.append(jsonDict)

result = []

for record in jsonList:
    id = record["id"]
    partial_split = id.split('_')
    u = partial_split[0]
    x = partial_split[2]

    # Find title
    url = f"https://api.kramerius.mzk.cz/search/api/client/v7.0/items/uuid:{u}/metadata/mods"
    response = requests.get(url)
    xml_data = response.content
    tree = convert_to_xml(xml_data)
    title_element = tree.find(".//mods:title", namespaces={"mods": "http://www.loc.gov/mods/v3"})
    if title_element is not None:
        title = title_element.text
    else:
        title = ""

    # Find date
    url_2 = f"https://api.kramerius.mzk.cz/search/api/client/v7.0/items/uuid:{x}/metadata/mods"
    response = requests.get(url_2)
    xml_data_2 = response.content
    tree_2 = convert_to_xml(xml_data_2)

    try:
        date_element = tree_2.find(".//mods:date", namespaces={"mods": "http://www.loc.gov/mods/v3"})
        if date_element is None:
            date_element = tree_2.find(".//mods:dateIssued", namespaces={"mods": "http://www.loc.gov/mods/v3"})
    except:
        date_element = None

    if date_element is not None:
        date = date_element.text
    else:
        date = ""

    result.append({"uuid": id, "title": title, "date": date})

    print({"uuid": id, "title": title, "date": date})

with open('periodicals_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
