#!/usr/bin/env bash

for i in $(seq 1 100);do
    echo book_${i}.txt
    wget -O book_${i}.txt https://www.gutenberg.org/files/${i}/${i}-0.txt
    hdfs dfs -put book_${i}.txt
    rm book_${i}.txt
done