#!/bin/bash

echo "Installing requirements..."
python -m pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null
echo "Requirements installed"