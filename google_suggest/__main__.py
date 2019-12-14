#!/usr/bin/env python


def main():
    import argparse
    import re
    from typing import List
    from .core import fetch_suggestion

    arg_parser = argparse.ArgumentParser(
            prog = __name__,
            usage = 'usage',
            description = 'description',
            add_help = True,
            )

    arg_parser.add_argument('keyword', help = 'keyword')

    args = arg_parser.parse_args()

    keyword: str = re.sub('[ 　]+', ' ', args.keyword)

    suggestions: List[str] = fetch_suggestion(keyword)

    print(suggestions)


if __name__ == '__main__':
    main()


