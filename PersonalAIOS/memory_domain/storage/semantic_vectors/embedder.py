import chromadb
import os
import logging

logger = logging.getLogger("SemanticVectors")

class SemanticVectors:
    """
    Lightweight embeddings for abstract relationships.
    Uses a local ChromaDB instance to find 'vibes' or thematic matches
    when exact regex or BM25 fails. Zero cloud reliance for memory.
    """
    def __init__(self, db_path="~/.personalos/memory_graph/vectors"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(self.db_path, exist_ok=True)

        # Initialize local persistent Chroma DB
        self.client = chromadb.PersistentClient(path=self.db_path)

        # Uses default sentence-transformers model automatically
        self.collection = self.client.get_or_create_collection(name="obsidian_graph")
        logger.info("Local Semantic Vector DB Initialized.")

    def embed_and_store(self, text: str, node_id: str, metadata: dict = None):
        """Converts text to vector and associates it with a Markdown node."""
        if not metadata:
            metadata = {"source": "obsidian"}

        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[node_id]
        )
        logger.debug(f"Embedded node {node_id} into Semantic DB.")

    def search_similar(self, query: str, n_results: int = 3) -> list:
        """
        Finds the closest matching nodes conceptually. Returns node IDs.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results.get("ids", [[]])[0]
