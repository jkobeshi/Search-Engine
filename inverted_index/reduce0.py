#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    count = key
    group = list(group)
    count = 0
    for line in group:
        line = line.split("\n")[0].split("\t")[1]
        count += int(line)
    return count


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    count = 0
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        count += reduce_one_group(key, group)
    print(f"{count}")


if __name__ == "__main__":
    main()
