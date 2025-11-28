"""
utils.py

Utility functions for text preprocessing.
"""

import re


# Small, built-in stopword list to avoid extra dependencies.
_BASIC_STOPWORDS = set(
    """
    a an the and or but if while is are was were be been being to of in on at for
    with without about into over after before between out up down from as by this
    that these those it its their his her they them we us you i
    """.split()
)


def split_sentences(text: str):
    """
    Very simple sentence splitter based on punctuation.
    Good enough for short news snippets/headlines.
    """
    if not text:
        return []

    # Split on ., ?, ! followed by whitespace
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # Remove empty strings and trim
    return [s.strip() for s in sentences if s.strip()]


def tokenize(text: str, lowercase: bool = True, remove_stopwords: bool = True):
    """
    Tokenize text into word tokens.
    """
    if lowercase:
        text = text.lower()
    tokens = re.findall(r"\b\w+\b", text)
    if remove_stopwords:
        tokens = [t for t in tokens if t not in _BASIC_STOPWORDS]
    return tokens
