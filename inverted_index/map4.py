#!/usr/bin/env python3
"""Group by partition."""
import sys

for line in sys.stdin:
    line = line.split("\n")[0].split("\t")
    doc_id = line[0]

    value = line[1].split(" ")
    term = value[0]
    idfk = value[1]
    tfik = value[2]
    d_i = value[3]

    print(f"{term} {idfk} {int(doc_id) % 3}\t{doc_id} {tfik} {d_i}")
