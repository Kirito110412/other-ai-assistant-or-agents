#!/usr/bin/env bash
# Universal Setup Script for PersonalAIOS

echo "Initializing PersonalAIOS Environment..."

# 1. Create directory structure
mkdir -p ~/.personalos/memory_graph
mkdir -p ~/.personalos/identity
mkdir -p ~/.personalos/goals

echo "[OK] Created local ~/.personalos directories."

# 2. Check for Docker
if ! command -v docker &> /dev/null
then
    echo "[WARNING] Docker could not be found. The Sandbox Orchestrator will be disabled."
else
    echo "[OK] Docker is installed."
fi

# 3. Check for Ollama
if ! command -v ollama &> /dev/null
then
    echo "[WARNING] Ollama is not installed locally. Heavy routing will default to Cloud models."
else
    echo "[OK] Ollama is installed."
    # Optionally pull default model here if ollama is running
    # ollama pull llama3
fi

echo "Setup Complete! You may now run the Onboarding Wizard to initialize your AI."
