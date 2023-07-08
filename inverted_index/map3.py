#!/usr/bin/env python3
"""Group by term."""
import sys
# job - calculate for every doc - wik and di

# term doc_id idfk tfik
# cool	1 0.47712125471966244 1
for line in sys.stdin:
    line = line.split("\n")[0].split("\t")
    term = line[0]
    value = line[1].split(" ")
    doc_id = value[0]
    n_k = value[1]
    count = value[2]
    print(f"{doc_id}\t{term} {n_k} {count}")
