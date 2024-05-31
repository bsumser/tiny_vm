#!/bin/sh
if [ -f "$1" ]; then
    echo "Compiling $1"
    python3 grammar.py $1 
fi