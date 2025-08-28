#!/bin/bash
set -e

# Install Python & libaio (tries dnf, falls back to apt)
if command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y python3 python3-pip libaio
elif command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3 python3-pip libaio1
fi

pip3 install -r requirements.txt

echo "✅ Python environment ready."

