import re
from xml.etree import ElementTree
from typing import List
import requests
import asyncio
import aiohttp
from .keyword import Keyword
from .suggestion import Suggestion


extention_chars = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんabcdefghijklmnopqrstuvwxyz1234'


def fetch_suggestion(keyword: str, ext: bool = False):
    keywords = [ Keyword(keyword) ]

    if ext:
        keywords += [ Keyword(keyword, ch) for ch in extention_chars ]

    future = _create_future_of_fetching_suggestion(keywords)

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(future)

    return result


async def _create_future_of_fetching_suggestion(keywords):
    async with aiohttp.ClientSession(
            connector = aiohttp.TCPConnector(
                limit = 10,
                limit_per_host = 30,
                ),
            ) as session:
        futures = [ _request(k, session) for k in keywords ]
        return await asyncio.gather(*futures)


async def _request(keyword: Keyword, session, timeout_sec: int = 10):
    async with session.get(f'https://www.google.com/complete/search',
            params = { 'hl': 'ja', 'output': 'toolbar', 'q': keyword.to_str() },
            raise_for_status = True,
            timeout = timeout_sec,
            ) as response:
        suggestion_words: List[str] = _parse_xml(await response.text())
        return Suggestion(keyword, suggestion_words)


def _parse_xml(xml: str) -> List[str]:
    root = ElementTree.fromstring(xml)
    completeSuggestionTags = root.findall('CompleteSuggestion')
    return [ suggestion.find('suggestion').get('data') for suggestion in root.findall('CompleteSuggestion') ]


