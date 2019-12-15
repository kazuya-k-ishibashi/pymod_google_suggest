from typing import List
import re
import requests
from xml.etree import ElementTree


def fetch_suggestion(keyword: str) -> List[str]:
    keyword = _shape_request_data(keyword)
    response = _request(keyword)
    return _parse(response)


def _shape_request_data(keyword: str) -> str:
    return re.sub('[ 　]+', '+', keyword)


def _request(keyword: str):
    response = requests.get(f'https://www.google.com/complete/search?hl=ja&output=toolbar&q={keyword}')
    response.raise_for_status()
    return response


def _parse(response) -> List[str]:
    xml: str = response.text
    root = ElementTree.fromstring(xml)
    completeSuggestionTags = root.findall('CompleteSuggestion')
    return [ suggestion.find('suggestion').get('data') for suggestion in root.findall('CompleteSuggestion') ]


