#!/bin/sh
if [ -f "$1" ]; then
    echo "$1" exists
    python3 grammar.py $1 
fi