# Concurrency & CNS Model

## Overview
The Central Nervous System (CNS) solves the primary drawback of Isolated Functional Modules: inter-process communication latency.

## Architecture
1.  **Event Bus (`event_bus.py`)**
    *   A high-speed Pub/Sub message broker.
    *   Example: The `Screen Listener` publishes an anomaly; the `Logic Engine` subscribes to anomalies, instantly waking up to process the event.
2.  **Task Coordinator (`task_coordinator.py`)**
    *   Dynamically binds isolated modules temporarily to achieve complex user goals.
    *   Example Request: "Research this topic and format it for my email."
    *   *Execution*: Coordinator simultaneously fires up the Research Scraper, allocates Short-term Memory, and wakes up the Email Surrogate module, feeding outputs across the Event Bus seamlessly.
