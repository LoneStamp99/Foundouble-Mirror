#!/bin/bash

while true; do
    read -r -p "Which file do you want to run? Enter 0.111 for Ruby or 0.222 for Python: " Selection
    if [ "$Selection" == "0.111" ]; then
        if command -v ruby > /dev/null; then
            ruby foundmir/foundoublemirror/Program.rb
            exit
        else
            echo "Ruby is not installed."
        fi
    elif [ "$Selection" == "0.222" ]; then
        python foundmir/foundoublemirror/data/main.py
        exit
    else
        echo "Invalid selection."
    fi
done