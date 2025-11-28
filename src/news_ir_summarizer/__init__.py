"""
news_ir_summarizer

Package exposing the news search engine and summarizer.
"""

from .engine import NewsSearchEngine
from .summarizer import SimpleSummarizer

__all__ = ["NewsSearchEngine", "SimpleSummarizer"]
