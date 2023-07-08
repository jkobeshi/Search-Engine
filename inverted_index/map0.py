#!/usr/bin/env python3
"""Map 0."""
import csv
import sys


csv.field_size_limit(sys.maxsize)


data = sys.stdin.readlines()

print(f"1\t{len(data)}")
