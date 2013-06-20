#!/lusr/bin/python

from XML import xml_find
from datetime import datetime
from sys import stdin, stdout, setrecursionlimit

# Set to true to display timing information
time = False

# Recursion limit is set to 1000 by default, which fails for
# very large XMLs. Increase it.
setrecursionlimit(100000)

# Call the main program and time it
t1 = datetime.now()
xml_find (stdin, stdout)
t2 = datetime.now()
if time:
    print str((t2-t1))
