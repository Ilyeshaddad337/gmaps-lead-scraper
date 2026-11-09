#!/bin/bash


# give the keywords as array

arr=(
"coffee shop constantine"
)
dirroctory="coffee_shops"
source .venv/bin/activate
for keyword in "${arr[@]}"; do
    echo "Running script for keyword: $keyword"
    python3 main.py "$keyword" "$dirroctory"
    if [ $? -ne 0 ]; then
        echo "Error occurred while processing keyword: $keyword"
        exit 1
    fi
done
