"""
summarizer.py

Simple frequency-based extractive summarization over a list of texts.
"""

import math
from collections import Counter

from .utils import split_sentences, tokenize


class SimpleSummarizer:
    """
    Very simple extractive summarizer:

    1. Concatenate input texts.
    2. Split into sentences.
    3. Compute word frequencies.
    4. Score sentences by sum of word frequencies (normalized by length).
    5. Return top-N sentences as the summary.
    """

    def __init__(self, min_sentence_length: int = 30):
        """
        :param min_sentence_length: Minimum character length of a sentence
                                   to be considered for scoring.
        """
        self.min_sentence_length = min_sentence_length

    def summarize(self, texts, max_sentences: int = 3) -> str:
        """
        Summarize a list of short texts (e.g., headlines or short snippets).

        :param texts: iterable of strings
        :param max_sentences: maximum number of sentences to include in summary
        :return: summary string
        """
        if not texts:
            return "(No documents to summarize.)"

        combined = " ".join(texts)
        sentences = split_sentences(combined)
        if not sentences:
            return "(No sentences found to summarize.)"

        # Build word frequency across all sentences
        word_freq = Counter()
        for s in sentences:
            word_freq.update(tokenize(s))

        if not word_freq:
            return "(Insufficient content for summarization.)"

        # Score sentences
        scored = []
        for i, s in enumerate(sentences):
            if len(s) < self.min_sentence_length:
                continue  # skip very short sentences
            tokens = tokenize(s)
            if not tokens:
                continue
            score = sum(word_freq[t] for t in tokens)
            # normalize by log sentence length to avoid heavy bias for long sentences
            norm = math.log(len(tokens) + 1)
            scored.append((i, score / norm, s))

        if not scored:
            # fallback: just return the first few sentences
            return " ".join(sentences[:max_sentences])

        # Sort by score descending; then pick top indices and restore original order
        scored.sort(key=lambda x: x[1], reverse=True)
        top_indices = sorted(idx for idx, _, _ in scored[:max_sentences])

        selected = [sentences[i] for i in top_indices]
        return " ".join(selected)
