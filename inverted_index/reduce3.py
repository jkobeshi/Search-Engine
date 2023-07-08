#!/usr/bin/env python3
"""
Reduce into partitions.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math


# print(f"{doc_id}\t{term} {n_k} {count}")
def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)

    big_n = 0
    with open("total_document_count.txt", "r", encoding="utf-8") as n_file:
        big_n = n_file.readlines()[0].split("\n")[0]

    d_i = 0
    new_group = []

    for line in group:
        value_line = line.split("\n")[0].split("\t")[1].split(" ")
        n_k = value_line[1]

        idfk = math.log(float(big_n)/float(n_k), 10)
        tfik = value_line[2]
        wik = float(idfk) * float(tfik)
        d_i += (wik * wik)
        new_group.append(f"{key}\t{value_line[0]} {idfk} {tfik}")

    for line in new_group:
        print(line + f" {d_i}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
