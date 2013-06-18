#!/lusr/bin/python

from sys import stdin, stdout
from xml.etree import ElementTree as ET

def read_input (r) :
    xml = ''
    read = r.readline()
    while not read == '' :
        xml = xml + read
        read = r.readline()
    return xml

def read_pair (r) :
    xml = read_input (r)
    root = ET.fromstring("<PAIR>" + xml + "</PAIR>")
    return {'xml': root[0], 'search': root[1]}

def read_pairs (r) :
    xml = read_input (r)
    root = ET.fromstring("<PAIRS>" + xml + "</PAIRS>")
    pairs = []
    for index in range(0,len(root),2) :
        if index+1 == len(root) :
            break
        pairs.append ({'xml': root[index], 'search': root[index+1]})
    return pairs

def find_recurse (xml, search) :
    if xml.tag == search.tag :
#        print xml.tag
        for i in range (len(search)) :
            for j in range (len(xml)) :
                if find_recurse (xml[j], search[i]) :
                    break
            else :
                return False
        return True
        """
        if len (search) == 0 :
            return True
        finds = [False]*len(search)
        for j in range (len(xml)) :
            for i in range (len(search)) :
                if not finds[i] :
                    finds[i] = find_recurse (xml[j], search[i])
            if not False in finds :
                break
        else :
            return False
        return True
        """
    else :
        return False

def find_matches (xml, search, xml_index, results) :
#    print str(xml_index) + '\t' + xml.tag
    if find_recurse (xml, search) :
        results.append (str(xml_index) + '\n')
    for index in range (len(xml)) :
        xml_index = find_matches (xml[index], search, xml_index + 1, results)
    return xml_index

def find_in_pair (pair, out) :
    results = []
    find_matches (pair['xml'], pair['search'], 1, results)
    out.append (str(len(results)) + '\n')
    out.extend (results)

def find_in_pairs (pairs, out) :
    for pair in pairs :
        out.extend (find_in_pair (pair, out))
        out.append('\n')

def xml_find (r, w) :
    pair = read_pair (r)
    result = []
    find_in_pair (pair, result)
    w.writelines (result)

def xml_find_multiple (r, w) :
    pairs = read_pairs (r)
    result = []
    find_in_pairs (pairs, result)
    w.writelines (result)

xml_find (stdin, stdout)
