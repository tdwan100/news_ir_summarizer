"""
interface.py

Command-line interface logic for the news search + summarization tool.
"""

import argparse

from .engine import NewsSearchEngine
from .summarizer import SimpleSummarizer


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="News headline search and summarization tool."
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to CSV file with a text column (default column name: 'headline').",
    )
    parser.add_argument(
        "--text-column",
        default="headline",
        help="Name of the text column in the CSV (default: 'headline').",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of top documents to retrieve for each query (default: 5).",
    )
    parser.add_argument(
        "--summary-sentences",
        type=int,
        default=3,
        help="Maximum number of sentences in the summary (default: 3).",
    )
    return parser


def interactive_loop(engine: NewsSearchEngine,
                     summarizer: SimpleSummarizer,
                     top_k: int = 5,
                     max_summary_sentences: int = 3):
    """
    Simple command-line interaction loop:
    - user types query
    - system prints top-k results
    - system prints a short summary over the top results
    """
    print("\n=== News Headline Search & Summarization Tool ===")
    print("Type a query and press Enter. Type 'exit' or 'quit' to leave.")

    while True:
        query = input("\nQuery: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Exiting.")
            break
        if not query:
            continue

        results = engine.search(query, top_k=top_k)
        if not results:
            print("No results found.")
            continue

        print(f"\nTop {len(results)} results:")
        top_texts = []
        for rank, idx, score, text in results:
            top_texts.append(text)
            print(f"[{rank}] (score={score:.4f}) {text}")

        summary = summarizer.summarize(top_texts, max_sentences=max_summary_sentences)
        print("\nSummary of top results:")
        print(summary)


def run_from_args(args: argparse.Namespace):
    """
    High-level entry point used by cli.py:
    - Initialize engine.
    - Load data.
    - Fit TF-IDF model.
    - Run interactive loop.
    """
    engine = NewsSearchEngine(text_column=args.text_column)
    engine.load_data(args.csv)
    engine.fit()

    summarizer = SimpleSummarizer()
    interactive_loop(
        engine,
        summarizer,
        top_k=args.top_k,
        max_summary_sentences=args.summary_sentences,
    )
