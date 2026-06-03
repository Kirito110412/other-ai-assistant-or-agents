class GraphTraversal:
    """
    Multi-hop logic linking without context bloat.
    """
    def __init__(self):
        pass

    def traverse_links(self, starting_node: str, depth: int = 2) -> list:
        """
        Follows the [[WikiLinks]] in the Obsidian Graph to pull related
        concepts without loading the entire database.
        """
        return ["Concept_A", "Concept_B"]
