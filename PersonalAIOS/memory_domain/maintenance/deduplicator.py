import os
import logging
from PersonalAIOS.core_engine.routing.hybrid_switch import hybrid_router

logger = logging.getLogger("Deduplicator")

class Deduplicator:
    """
    Merges overlapping conceptual nodes native to the Markdown structure.
    Runs asynchronously during the Sleep Cycle.
    """
    def __init__(self, storage_dir="~/.personalos/memory_graph"):
        self.storage_dir = os.path.expanduser(storage_dir)

    async def run_deduplication(self):
        """
        Scans for duplicate files or heavily overlapping vectors
        and rewrites them into a single coherent node.
        """
        logger.info("Initializing background memory deduplication...")

        if not os.path.exists(self.storage_dir):
            return

        md_files = [f for f in os.listdir(self.storage_dir) if f.endswith(".md")]

        # In a full implementation, we use SemanticVectors to group similar files first.
        # Here we mock finding two highly similar files to merge.
        if len(md_files) < 2:
            return

        file1 = os.path.join(self.storage_dir, md_files[0])
        file2 = os.path.join(self.storage_dir, md_files[1])

        with open(file1, 'r') as f: doc1 = f.read()
        with open(file2, 'r') as f: doc2 = f.read()

        prompt = (
            "You are the memory optimization engine. I will provide you with two raw memory nodes. "
            "Merge them into a single, highly compressed, coherent markdown file without losing facts. "
            f"Node 1:\n{doc1}\n\nNode 2:\n{doc2}"
        )

        messages = [{"role": "system", "content": prompt}]

        try:
            # Use local 3B model (complexity 0.2) to compress memory for free in the background
            merged_content = await hybrid_router.execute_query(messages, complexity=0.2)

            # Write the merged result back to file1 and delete file2
            with open(file1, 'w') as f:
                f.write(merged_content)
            os.remove(file2)

            logger.info(f"Successfully deduplicated {md_files[1]} into {md_files[0]}")

        except Exception as e:
            logger.error(f"Deduplication failed during Sleep Cycle: {e}")
