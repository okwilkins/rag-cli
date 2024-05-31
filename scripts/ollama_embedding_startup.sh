#!/bin/bash
# ollama_startup.sh

mkdir -p /home/ollama/logs
# Start the Ollama server to pull the phi3 model as the ollama service has to be running first
# A 5 second sleep is added to ensure the server is up and running before the model is pulled
ollama serve > /home/ollama/logs/server.log & sleep 5

# Pull the model only if it does not exist
nomic_model_path=/home/ollama/.ollama/models/manifests/registry.ollama.ai/library/nomic-embed-text/v1.5
if [ ! -f "$model_path" ]; then
    ollama pull nomic-embed-text:v1.5
fi

tail -f /home/ollama/logs/server.log