#!/bin/sh
TVMDIR=~/tiny_vm
if [ -f "$1" ]; then
    echo "Compiling $1"
    python3 compiler.py $1
    echo $?
    if [ $? -eq 0 ]; 
    then
        echo "success"
        python3 assemble.py QkAsm/qkmain.asm > ${TVMDIR}/OBJ/\$Main.json
        if [ $? -eq 0 ]; then
            bin/tiny_vm \$Main
        fi
    fi
fi
