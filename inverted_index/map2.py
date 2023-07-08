#!/usr/bin/env python3
"""Group by term."""
import sys

# n_k - find number of documents containing term
for line in sys.stdin:
    line = line.split("\n")[0].split(" ")
    term = line[0]
    value = line[1].split("\t")
    doc_id = value[0]
    count = value[1]
    print(f"{term}\t{doc_id} {count}")
