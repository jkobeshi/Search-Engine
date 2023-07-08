#!/usr/bin/env python3
"""
Reduce into partitions.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


# print(f"{term} {int(doc_id) % 3}\t{doc_id} {tfik} {d_i}")
def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)

    key_line = key.split(" ")
    term = key_line[0]
    idfk = key_line[1]
    partition = key_line[2]

    final_line = f"{partition}\t{term} {idfk}"
    for line in group:
        value = line.split("\n")[0].split("\t")[1]
        final_line += f" {value}"
    print(final_line)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
