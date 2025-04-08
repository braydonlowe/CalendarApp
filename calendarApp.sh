#!/bin/bash
echo "Starting Project"

read -p "Enter your username: " username
read -s -p "Enter your password: " password
echo

printf "%s\n%s" "$username" "$password" | python main.py

echo "Project exited"