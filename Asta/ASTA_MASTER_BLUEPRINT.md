# ASTA: Advanced Sentient Task Architecture - Master Blueprint

## 1. Core Philosophy & Design Axioms
Asta is not a collection of linear scripts or nested `if/else` statements. It is a continuous, stateful, localized AI Operating System designed around **Directed Acyclic Graphs (DAGs)**, **Hierarchical Paged Memory**, and **Strict Resource Sandboxing**. It acts as a cognitive framework enabling a 3B parameter local LLM to execute complex, multi-day tasks safely.

### Axioms
1. **Zero-Placeholder Guarantee:** No logic is mocked. If a system claims to research, it must physically actuate the browser or API.
2. **Infinite Context via OS Paging:** The LLM's context window is L1 Cache. Obsidian is the Hard Drive. Letta-style memory management handles the swaps.
3. **Physical Surrogate Reality:** Asta does not rely on web APIs for interaction; it relies on VLM (Visual Language Model) coordinate mapping and physical mouse/keyboard actuation (Browser-Use paradigm).
4. **Standardized Protocols:** Tool usage is entirely abstracted via the Model Context Protocol (MCP), never hardcoded scripts.

---

## 2. Mathematical State Machine (The Core Engine)
Asta's execution loop is modeled after a continuous Markov Decision Process (MDP).

### 2.1 State Representation
At any time $t$, the system state $S_t$ is a tuple:
$$S_t = (M_{active}, E_{docker}, T_{pending}, O_{visual}, P_{mcp})$$
Where:
- $M_{active}$: Paged context currently loaded in the LLM's prompt.
- $E_{docker}$: Status of the isolated OpenHands-style development container.
- $T_{pending}$: The DAG of pending sub-tasks.
- $O_{visual}$: The current bounding-box matrix of the screen.
- $P_{mcp}$: Active Model Context Protocol server connections.

### 2.2 The Graph Router (Replacing `if/else`)
Asta utilizes a LangGraph-style workflow. Every task $T$ is decomposed into nodes $n_i \in N$ and directed edges $e_{ij} \in E$.
- **Node Execution:** $n_i(S_t) \rightarrow S_{t+1}$
- **Conditional Edges:** Probability functions determine the next node based on LLM output and verification scripts. If a task fails verification, the graph transitions to an explicit error-correction node, never a generic `catch`.

---

## 3. Hierarchical Paged Memory (The Letta / Mem0 Paradigm)
To run a 3B model without Out-Of-Memory (OOM) errors, Asta implements Virtual Memory.

### 3.1 Memory Tiers
1. **L1 (Context Window):** The immediate prompt. Max 4,000 tokens.
2. **L2 (Vector/Semantic Cache):** Qdrant-backed similarity search for immediate task relevance.
3. **L3 (Obsidian Graph):** The hard drive. Markdown files linked via Bi-directional references.

### 3.2 The Paging Algorithm
Let $C_{max}$ be the maximum token limit. When evaluating a prompt $P_{raw}$:
1. Extract Entities: $E = \text{NER}(P_{raw})$
2. Query L3 Obsidian Graph for relevant nodes $N_E$.
3. If $|N_E| + |P_{raw}| > C_{max}$:
   - Trigger **Eviction Protocol**: Archive oldest dialogue turns to L3.
   - Summarize context using a lossless semantic compressor (SimpleMem architecture).
4. Load necessary context into L1.

---

## 4. Actuation & Sensory Pipeline (The Browser-Use Paradigm)
Asta interacts with the world visually, not programmatically.

### 4.1 Visual Parsing (VLM Bounding Boxes)
1. **Screenshot Capture:** System captures image $I$.
2. **DOM / UI Tree Extraction:** System analyzes $I$ and generates bounding boxes $B_k = (x_1, y_1, x_2, y_2)$ for all interactable elements.
3. **Semantic Mapping:** The VLM tags each $B_k$ (e.g., `<button id=14>Login</button>`).

### 4.2 Motor Control
When the LLM decides to click "Login" (Target ID 14):
1. Retrieve center coordinates: $C_{14} = (\frac{x_1+x_2}{2}, \frac{y_1+y_2}{2})$
2. Inject human-like Bezier curve mouse movement to $C_{14}$.
3. Execute hardware-level OS click.

---

## 5. Security & Isolation (The OpenHands Paradigm)
Asta generates its own skills (Python scripts). These must be sandboxed.

### 5.1 The Persistent DevEnv
- All agent-generated code is executed inside a long-living Docker container (`asta_devenv_XYZ`).
- **No Path Traversal:** Strict volume binding (`/workspace`) with absolute path verification enforcing `full_path.startswith(host_vol_path)`.
- **PTY Streaming:** WebSockets are used to stream real-time ANSI terminal output from the container to the agent, allowing it to respond to interactive prompts (`npm install` -> `[y/N]`).

---

## 6. SOTA Architecture Gap & Integration Roadmap
To build Asta properly from scratch, any future session must prioritize these core modules over feature scripts:

1. **Implement `AstaGraph`:** Build the directed graph executor (NetworkX or LangGraph clone) to handle task routing.
2. **Implement `MemoryPager`:** Build the L1/L2/L3 paging system to prevent context overflow.
3. **Integrate `MCPClient`:** Connect Asta to `modelcontextprotocol/servers` so it can natively use Postgres, Github, etc.
4. **Implement `VLMActuator`:** Connect a local vision model (e.g., LLaVA) to PyAutoGUI for semantic screen interaction.

*This blueprint guarantees Asta is built as an enterprise-grade AI operating system, strictly adhering to the architectural standards of LangGraph, Letta, OpenHands, and Browser-Use.*
