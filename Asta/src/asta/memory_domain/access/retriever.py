import os
import re
from rank_bm25 import BM25Okapi

class ExactParagraphRetriever:
    """
    Ultra-fast exact paragraph fetcher.
    Uses BM25 to pull ONLY the exact paragraphs needed out of the Obsidian Graph,
    preventing context window bloat and keeping VRAM usage at zero.
    """
    def __init__(self, storage_dir="~/.personalos/memory_graph"):
        self.storage_dir = os.path.expanduser(storage_dir)
        self.corpus = []
        self.paragraphs = []

    def _load_corpus(self):
        """Loads all Markdown nodes and splits them into discrete paragraphs."""
        self.corpus = []
        self.paragraphs = []

        if not os.path.exists(self.storage_dir):
            return

        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(self.storage_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Split node by Markdown headers or double linebreaks
                parts = re.split(r'\n\n|\n#+ ', content)
                for part in parts:
                    clean_part = part.strip()
                    if len(clean_part) > 10: # Ignore tiny fragments
                        self.paragraphs.append(clean_part)
                        # Tokenize for BM25
                        self.corpus.append(clean_part.lower().split())

    def fetch_exact_context(self, query: str, top_k: int = 1) -> str:
        """
        Calculates BM25 mathematically to find the single most relevant
        paragraph across the entire memory graph instantly.
        """
        self._load_corpus()
        if not self.corpus:
            return "No memory context found."

        tokenized_query = query.lower().split()
        bm25 = BM25Okapi(self.corpus)

        # Get exact top_k paragraphs mathematically
        top_paragraphs = bm25.get_top_n(tokenized_query, self.paragraphs, n=top_k)

        if top_paragraphs:
            return "\n\n---\n\n".join(top_paragraphs)
        return "No relevant context found in memory."
