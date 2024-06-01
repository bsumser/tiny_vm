#!/bin/sh
for file in ./test_progs/*.qk
do
  ./quack.sh "$file"
done