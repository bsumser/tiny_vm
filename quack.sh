#!/bin/sh
if [ -f "$1" ]; then
    echo "Compiling $1"
    python3 compiler.py $1 
fi
