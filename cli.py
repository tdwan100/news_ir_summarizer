"""
cli.py

Convenience entry point for running the news IR + summarization tool.

Example:
    python cli.py --csv data/example_news.csv --text-column headline
"""

import os
import sys

# Make sure the 'src' directory is on sys.path so we can import the package
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from news_ir_summarizer.interface import build_arg_parser, run_from_args  # noqa: E402


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    run_from_args(args)


if __name__ == "__main__":
    main()
