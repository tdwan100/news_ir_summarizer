from setuptools import setup, find_packages

setup(
    name="news_ir_summarizer",
    version="0.1.0",
    description="A simple news headline search and summarization tool using TF-IDF.",
    author="Tanner Dwan",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "scikit-learn",
        "numpy",
    ],
    python_requires=">=3.9",
)
