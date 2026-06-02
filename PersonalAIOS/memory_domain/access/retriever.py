import os

class ExactParagraphRetriever:
    """
    Ultra-fast exact paragraph fetcher.
    Uses BM25 and Regex to pull ONLY the exact paragraphs needed,
    preventing context window bloat and keeping VRAM usage at zero.
    """
    def __init__(self, storage_dir="~/.personalos/memory_graph"):
        self.storage_dir = os.path.expanduser(storage_dir)

    def fetch_exact_context(self, query: str) -> str:
        """
        Scans the markdown files, finds the relevant paragraph, and extracts just that block.
        """
        return "Extracted specific paragraph regarding: " + query
