#!/bin/bash
echo "Starting Project"

read -p "Enter your username: " username
read -s -p "Enter your password: " password
echo

python main.py "$username" "$password"

echo "Project exited"