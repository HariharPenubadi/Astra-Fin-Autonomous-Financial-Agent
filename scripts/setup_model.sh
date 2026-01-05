#!/bin/bash
echo "--- Setting up Astra-Fin Model ---"

if ! command -v ollama &> /dev/null; then
    echo "Error: Ollama is not installed."
    exit 1
fi

ollama create astra-fin -f Modelfile
echo "--- Model Deployed Locally ---"