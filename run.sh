#!/bin/bash

# Source the virtual environment
. ./.venv/Scripts/activate

# Load environment variables from the .env file in the app directory if it exists
if [ -f ./.env ]; then
    . ./.env
else
    echo ".env file not found, proceeding without loading environment variables."
fi

# Set PYTHONPATH to the parent directory of app
export PYTHONPATH=$(pwd)

python app/main.py
