import os

class ObsidianGraphStorage:
    """
    Zero-VRAM, interconnected markdown file nodes.
    """
    def __init__(self, storage_dir="~/.personalos/memory_graph"):
        self.storage_dir = os.path.expanduser(storage_dir)
        os.makedirs(self.storage_dir, exist_ok=True)

    def write_node(self, node_id: str, content: str, links: list):
        """
        Writes a discrete memory node.
        Links represent the edges in the knowledge graph (e.g., [[User_Preferences]]).
        """
        filepath = os.path.join(self.storage_dir, f"{node_id}.md")
        link_str = "\n".join([f"[[{link}]]" for link in links])

        with open(filepath, 'w') as f:
            f.write(content + "\n\n" + link_str)
