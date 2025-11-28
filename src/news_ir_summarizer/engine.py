"""
engine.py

TF-IDF based news search engine.
"""

from typing import List, Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class NewsSearchEngine:
    """
    Simple news search engine using TF-IDF + cosine similarity.
    """

    def __init__(self, text_column: str = "headline", max_features: int = 10000):
        """
        :param text_column: name of the column in the CSV that contains text.
        :param max_features: maximum vocabulary size for TF-IDF.
        """
        self.text_column = text_column
        self.max_features = max_features
        self.vectorizer = None
        self.doc_matrix = None
        self.docs = None

    def load_data(self, csv_path: str):
        """
        Load news data from a CSV file.

        CSV must contain a text column (default 'headline').
        Rows with missing values in that column are dropped.
        """
        df = pd.read_csv(csv_path)
        if self.text_column not in df.columns:
            raise ValueError(
                f"CSV must contain a '{self.text_column}' column. "
                f"Available columns: {list(df.columns)}"
            )
        df = df.dropna(subset=[self.text_column])
        # store the text as a simple list of strings
        self.docs = df[self.text_column].astype(str).tolist()
        print(f"[Engine] Loaded {len(self.docs)} documents from {csv_path}.")

    def fit(self):
        """
        Fit a TF-IDF vectorizer on the loaded documents.
        """
        if self.docs is None:
            raise RuntimeError("[Engine] No documents loaded. Call load_data() first.")

        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            ngram_range=(1, 2),  # unigrams + bigrams
            stop_words="english",
        )
        self.doc_matrix = self.vectorizer.fit_transform(self.docs)
        print("[Engine] TF-IDF model fitted on documents.")

    def search(self, query: str, top_k: int = 5) -> List[Tuple[int, int, float, str]]:
        """
        Search for the most relevant documents for a query.

        :param query: search query string
        :param top_k: number of top documents to return
        :return: list of tuples (rank, doc_index, score, text)
        """
        if self.vectorizer is None or self.doc_matrix is None:
            raise RuntimeError("[Engine] Model not fitted. Call fit() first.")

        query_vec = self.vectorizer.transform([query])
        # cosine similarity via dot product (TF-IDF vectors are L2-normalized)
        scores = linear_kernel(query_vec, self.doc_matrix).flatten()
        top_indices = scores.argsort()[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, start=1):
            results.append((rank, int(idx), float(scores[idx]), self.docs[idx]))
        return results
