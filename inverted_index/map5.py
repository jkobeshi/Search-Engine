#!/usr/bin/env python3
"""Group by partition."""
import sys

for line in sys.stdin:
    line = line.split("\n")[0]
    print(f"{line}")
