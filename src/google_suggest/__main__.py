#!/usr/bin/env python


def main():
    args = parse_args()

    suggestions = fetch_suggestion(args.keyword, args.ext, args.recurse_level)

    as_json = [
        {
            'keyword': {
                'original': s.keyword.original,
                'additional': s.keyword.additional if not s.keyword.additional == None else '',
            },
            'recurse_level': s.recurse_level,
            'words': s.words
        } for s in suggestions
    ]
    print(json.dumps(as_json, ensure_ascii = False))


def parse_args():
    arg_parser = argparse.ArgumentParser(
            prog = __name__,
            usage = 'usage',
            description = 'description',
            add_help = True,
            )

    arg_parser.add_argument('keyword', help = 'keyword')
    arg_parser.add_argument('-e', '--ext', help = 'ext', action='store_true')
    arg_parser.add_argument('-r', '--recurse_level', help = 'recurse', type = int, default = 1)

    args = arg_parser.parse_args()

    return args


if __name__ == '__main__':
    import re
    import json
    import argparse
    from typing import List
    from .google_suggest import fetch_suggestion

    main()


