#!/lusr/bin/python

MAX_TAGS = 12500
tag_names = ['ab', 'cd', 'ef', 'gh', 'ij']

from random import random, randint
from sys import stdout, setrecursionlimit
from xml.etree import ElementTree as ET

def generate_tag (tag_names) :
    return tag_names[randint(0,4)]

def generate_recurse (node, depth, count, MAX_TAGS, tag_names, termProb) :
#    print str(count) + '\t' + str(depth)
    if count == MAX_TAGS :
        return (count, False)
    if random() < termProb :
        return (count, True)

    children = randint (1,5)
    taken = []
    children_names = []
    for i in xrange(children) :
        child_name = generate_tag (tag_names)
        while child_name in children_names :
            child_name = generate_tag (tag_names)
        children_names.append (child_name)

#    print node.tag + '\t' + str(children_names) + '\n'
    for t in children_names :
        child = ET.SubElement (node, t)
        (count, status) = generate_recurse (child, depth + 1, count + 1, MAX_TAGS, tag_names, termProb)
        if not status :
            break

    return (count, status)

def pretty_print (node, depth) :
    if len(node) == 0 :
        print ''*depth + '<' + node.tag + ' />'
    else :
        print ''*depth + '<' + node.tag + '>'
        for c in node :
            pretty_print (c, depth+1)
        print ''*depth + '</' + node.tag + '>'

setrecursionlimit (1000000)
tree = ET.parse ('inp')
root = ET.Element (generate_tag(tag_names))
generate_recurse (root, 0, 0, MAX_TAGS, tag_names, 0.3)
pretty_print (root, 0)
print '<ab><cd></cd><ef/></ab>'
