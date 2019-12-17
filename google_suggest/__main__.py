#!/usr/bin/env python


def main():
    import argparse
    import re
    import json
    from typing import List
    from .core import fetch_suggestion

    arg_parser = argparse.ArgumentParser(
            prog = __name__,
            usage = 'usage',
            description = 'description',
            add_help = True,
            )

    arg_parser.add_argument('keyword', help = 'keyword')
    arg_parser.add_argument('-e', '--ext', help = 'ext', action='store_true')

    args = arg_parser.parse_args()

    suggestions = fetch_suggestion(args.keyword, args.ext)

    as_json = [
        {
            'keyword': {
                'original': s.keyword.original,
                'additional': s.keyword.additional if not s.keyword.additional == None else '',
            },
            'words': s.words
        } for s in suggestions
    ]
    print(json.dumps(as_json))


if __name__ == '__main__':
    main()


