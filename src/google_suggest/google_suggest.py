import re
from xml.etree import ElementTree
from typing import List
import requests
import asyncio
import aiohttp
from .keyword import Keyword
from .suggestion import Suggestion


extention_chars = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんabcdefghijklmnopqrstuvwxyz1234'


def fetch_suggestion(keyword: str, ext: bool = False, recurse_level: int = 1):
    if recurse_level < 1:
        recurse_level = 1
    if recurse_level > 3:
        recurse_level = 3

    all_suggestions = _fetch(keyword, ext, recurse_level, 1, [])

    return all_suggestions


def _fetch(keyword: str, ext: bool, recurse_level: int, current_level: int, all_suggestions: List[Suggestion]):
    keywords = [ Keyword(keyword) ]
    if ext:
        keywords += [ Keyword(keyword, ch) for ch in extention_chars ]

    future = _create_future_of_fetching_suggestion(keywords, current_level)

    loop = asyncio.get_event_loop()
    suggestions = loop.run_until_complete(future)
    all_suggestions += suggestions

    if current_level < recurse_level:
        for s in suggestions:
            for w in s.words:
                _fetch(w, ext, recurse_level, current_level + 1, all_suggestions)

    return all_suggestions

async def _create_future_of_fetching_suggestion(keywords: List[Keyword], level: int):
    async with aiohttp.ClientSession(
            connector = aiohttp.TCPConnector(
                limit = 10,
                limit_per_host = 30,
                ),
            ) as session:
        futures = [ _request(k, level, session) for k in keywords ]
        return await asyncio.gather(*futures)


async def _request(keyword: Keyword, level: int, session, timeout_sec: int = 10):
    async with session.get(f'https://www.google.com/complete/search',
            params = { 'hl': 'ja', 'output': 'toolbar', 'q': keyword.to_str() },
            raise_for_status = True,
            timeout = timeout_sec,
            ) as response:
        suggestion_words: List[str] = _parse_xml(await response.text())
        suggestion_words = [ w for w in suggestion_words if not w == keyword.to_str() ]
        return Suggestion(keyword, level, suggestion_words)


def _parse_xml(xml: str) -> List[str]:
    root = ElementTree.fromstring(xml)
    completeSuggestionTags = root.findall('CompleteSuggestion')
    return [ suggestion.find('suggestion').get('data') for suggestion in root.findall('CompleteSuggestion') ]


