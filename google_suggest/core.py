from typing import List
import re
import requests
from xml.etree import ElementTree


def fetch_suggestion(keyword) -> List[str]:
    keyword: str = re.sub('[ 　]+', '+', keyword)
    response = requests.get(f'https://www.google.com/complete/search?hl=ja&output=toolbar&q={keyword}')
    response.raise_for_status()

    suggests_xml: str = response.text
    root = ElementTree.fromstring(suggests_xml)
    return [ suggestion.find('suggestion').get('data') for suggestion in root.findall('CompleteSuggestion') ]


