#!/lusr/bin/python

from XML import xml_find
from datetime import datetime
from sys import stdin, stdout, setrecursionlimit

time = False

setrecursionlimit(100000)
t1 = datetime.now()
xml_find (stdin, stdout)
t2 = datetime.now()
if time:
    print str((t2-t1))
