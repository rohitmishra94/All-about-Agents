#!/bin/bash

# apt-get update
# apt install tmux -y
# curl -fsSL https://ollama.com/install.sh | sh
# ollama serve

# # tmux new-session -d "ollama run llama3-groq-tool-use --keepalive 60m"
# # tmux attach-session



# Update package list
apt-get update

# Install tmux
apt install tmux -y

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
# tmux new-session -d -s ollama-server "ollama serve"

# Create a new detached tmux session and run the Ollama command
# tmux new-session -d -s ollama-session "ollama run qwen2.5:14b --keepalive 1m"

# Optionally, reattach to the tmux session to check the output
# tmux attach-session -t ollama-session
# pip3 install ipykernel
# ipython kernel install --user --name=ola
# export OLLAMA_MODELS=/workspace/ola
# ollama run qwen2.5:14b --keepalive -1 
# https://github.com/ollama/ollama/blob/main/docs/faq.md#where-are-models-stored

# sudo systemctl list-units --type=service | grep your_process_name
# sudo systemctl stop your_service
# sudo systemctl disable your_service
