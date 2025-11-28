# News Headline Search and Summarization Tool

Lightweight information-retrieval and extractive summarization over a CSV of news headlines (or any short texts). It uses classic TF-IDF + cosine similarity for search and a frequency-based summarizer for quick, local usage—no external APIs or LLMs required.

## Quick start (how to use)

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
   Or install in editable mode: `pip install -e .`
2. Prepare a CSV with a text column (default name: `headline`). Remove empty rows if possible.
3. Run the interactive CLI:
   ```bash
   python cli.py --csv path/to/news.csv --text-column headline --top-k 5 --summary-sentences 3
   ```
   Type queries at the prompt; type `exit` or `quit` to leave.

### API usage
```python
from news_ir_summarizer import NewsSearchEngine, SimpleSummarizer

engine = NewsSearchEngine(text_column="headline")
engine.load_data("data/news.csv")
engine.fit()

results = engine.search("federal reserve", top_k=5)
texts = [text for _, _, _, text in results]

summarizer = SimpleSummarizer()
summary = summarizer.summarize(texts, max_sentences=3)
print(summary)
```

## Implementation (how it works)

- Files of interest:
  - `src/news_ir_summarizer/engine.py`: `NewsSearchEngine` loads the CSV with pandas, drops empty rows, builds a TF-IDF matrix (unigrams + bigrams, English stopwords, configurable `max_features`), and scores queries via cosine similarity (`linear_kernel`). Returns `(rank, doc_index, score, text)` tuples.
  - `src/news_ir_summarizer/summarizer.py`: `SimpleSummarizer` concatenates top documents, splits into sentences, scores sentences by word frequency (normalized by sentence length), and returns the best N sentences. Uses `utils.split_sentences` and `utils.tokenize` for simple regex-based processing and a small built-in stopword list.
  - `src/news_ir_summarizer/interface.py`: Builds CLI args, wires the engine and summarizer, and runs the interactive loop.
  - `cli.py`: Thin entry point that imports the package and starts the CLI.
- Pipeline:
  1) Load CSV and keep only the target text column.
  2) Fit TF-IDF on all documents.
  3) For each query, compute cosine similarity and take the top-k hits.
  4) Summarize those hits with the frequency-based extractor.

## Notes and assumptions

- Designed for small/medium local datasets; everything stays in memory.
- English-focused defaults (stopwords and simple sentence splitting).
- Summaries are extractive: only sentences that already exist in the retrieved text are returned.
- There is no persistent index—restart to reload and refit the model.

## Optional tweaks

- Increase recall on short headlines by adjusting `--top-k` or `NewsSearchEngine(max_features=...)`.
- Change the text column name with `--text-column` (e.g., `title`, `text`).
- If your CSV has longer articles, raise `SimpleSummarizer(min_sentence_length=...)` to ignore very short sentences.
