# Memory Domain Specification

## Overview
The Memory Domain utilizes a completely zero-VRAM footprint approach. Instead of keeping a massive vector database or bloated context window loaded in memory, it leverages an "Obsidian Graph" structure—a local directory of heavily interconnected Markdown files.

## Subsectors & Behaviors
1.  **Storage Layers:**
    *   *Short-term Context*: Handles immediate conversation windows.
    *   *Obsidian Graph*: The permanent storage engine using `.md` files.
    *   *Semantic Vectors*: Lightweight abstract relationship mapping.
2.  **Access Layers:**
    *   *Retriever*: Fetches exact paragraphs via fast regex and BM25 to avoid overwhelming the LLM context limit.
    *   *Graph Traversal*: Links multi-hop conceptual logic instantly.
3.  **Maintenance Behaviors (The Sleep Cycle):**
    *   Runs when the CPU/AI is idle.
    *   *Deduplicator*: Fuses duplicated concepts natively.
    *   *Archiver*: Trims and compresses stale thoughts without losing the abstract lesson.
