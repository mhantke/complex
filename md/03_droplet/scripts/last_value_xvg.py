#!/usr/bin/env python
import sys
with open(sys.argv[1], "r") as f:
    print f.readlines()[-1][:-1].split(" ")[-1]
