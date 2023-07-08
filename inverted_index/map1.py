#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
import re


csv.field_size_limit(sys.maxsize)

stopDict = set()

with open("stopwords.txt", "r", encoding="utf-8") as stopfile:
    for line in stopfile:
        line = line.split("\n")[0]
        stopDict.add(line)

data = sys.stdin.readlines()

# Sorting term frequency by document.
for line in csv.reader(data):
    concatLine = line[1] + " " + line[2]
    cleanedLine = str(re.sub(r"[^a-zA-Z0-9 ]+", "", concatLine)).casefold()
    words = cleanedLine.split()
    for word in words:
        if len(word) != 0 and word not in stopDict:
            # key: word, val: docID \t 1
            print(f"{word} {line[0]}\t1")
