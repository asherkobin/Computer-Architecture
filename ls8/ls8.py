#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

cpu = CPU()
#n = sys.argv[1]
#n = "ls8/examples/print8.ls8"
n = "ls8/examples/mult.ls8"
cpu.load(n)
cpu.run()