#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve models..."
ollama pull gemma:2b
ollama pull mxbai-embed-large
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid