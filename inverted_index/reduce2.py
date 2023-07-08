#!/usr/bin/env python3
"""
Find number of docs with each term.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


# group is term
def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    n_k = len(group)
    # print(f"{term}\t{doc_id} {count}")
    for line in group:
        doc_id_n_count = line.split("\n")[0].split("\t")[1].split(" ")
        print(f"{key}\t{doc_id_n_count[0]} {n_k} {doc_id_n_count[1]}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
