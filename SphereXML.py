#!/lusr/bin/python

from sys import stdin, stdout, setrecursionlimit
from xml.etree import ElementTree as ET

def read_input (r) :
    xml = ''
    while True :
        read = r.readline()
        if read == '' :
            break
        xml = xml + read
    return xml

def read_pairs (r) :
    xml = read_input (r)
    root = ET.fromstring("<PAIRS>" + xml + "</PAIRS>")
    pairs = []
    for index in range(0,len(root),2) :
        if index+1 == len(root) :
            break
        pairs.append ({'xml': root[index], 'search': root[index+1]})
    return pairs

def build_index (xml, xml_index, indices, search_root_tag) :
    if xml.tag == search_root_tag :
        indices[xml_index] = [xml]
    for child in xml :
        xml_index = build_index (child, xml_index+1, indices, search_root_tag)
    return xml_index

def find_recurse (search, indices) :
    for index in indices.keys() :
        node = indices[index][-1]
        if not search.tag == node.tag :
            del(indices[index])
    
    if len(search) == 0 :
        return
    if len(indices) == 0 :
        return

    where = {}
    for i in search :
        where[i.tag] = {}
        for index in indices.keys() :
            node = indices[index][-1]
            if len(search) > len(node) :
                del(indices[index])
                continue
            for j in node :
                if j.tag == i.tag :
                    where[i.tag][index] = j
                    break
            else :
                del(indices[index])

    if len(indices) == 0 :
        return

    for i in search :
        for index in indices.keys() :
            indices[index].append (where[i.tag][index])
        find_recurse (i, indices)
        for index in indices.keys() :
            indices[index].pop()         

def find_in_pair (pair, out) :
    results = []
    indices = {}
    xml = pair['xml']
    search = pair['search']
    build_index (xml, 1, indices, search.tag)
    find_recurse (search, indices)
    keys = indices.keys()
    keys.sort()
    results.append(str(len(indices)) + '\n')
    for i in keys :
        results.append (str(i) + '\n')
    out.extend (results)

def find_in_pairs (pairs, out) :
    for pair in pairs :
        find_in_pair (pair, out)
        out.append('\n')
    out.pop()

def xml_find (r, w) :
    pairs = read_pairs (r)
    result = []
    find_in_pairs (pairs, result)
    w.writelines (result)

setrecursionlimit(100000)
xml_find (stdin, stdout)
