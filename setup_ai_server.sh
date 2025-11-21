#!/usr/bin/env bash
set -e
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
echo 'Setup complete. Place models in laptop_ai_brain/models and run python laptop_ai_brain/main_ai_server.py'
