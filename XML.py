#!/lusr/bin/python

from xml.etree import ElementTree as ET

debug = False
verbose = False

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
    if (debug) :
        print xml
    root = ET.fromstring("<PAIRS>" + xml + "</PAIRS>")
    pairs = []
    for index in range(0,len(root),2) :
        if index+1 == len(root) :
            break
        pairs.append ({'xml': root[index], 'search': root[index+1]})
    return pairs

def build_index (xml, xml_index, indices, search_root_tag) :
    if (debug):
        print str(xml_index) + '\t' + xml.tag
    if xml.tag == search_root_tag :
        indices[xml_index] = [xml]
    for child in xml :
        xml_index = build_index (child, xml_index+1, indices, search_root_tag)
    return xml_index

def find_recurse (search, indices) :
    if (debug) :
        print search.tag
        if (verbose) :
            print indices
    for index in indices.keys() :
        if (debug) :
            print str(index) + '\t' + str(indices[index])
        node = indices[index][-1]
        if not search.tag == node.tag :
            if (debug):
                print '[F] Unequal'
            del(indices[index])
            continue
        if len(search) > len(node) :
            if (debug) :
                print '[F] Search node has more children at ' + str(index)
            del(indices[index])
    
    if len(search) == 0 :
        if (debug) :
            print 'Lowest level!'
        return
    if len(indices) == 0 :
        if (debug) :
            print 'All search objects empty'
        return

    where = {}
    for index in indices.keys() :
        where[index] = {}
        node = indices[index][-1]
        for i in search :
            child = node.find (i.tag)
            if child == None :
                if (debug) :
                    print '[F] %s not found at %d' % (i.tag, index)
                del(indices[index])
                del(where[index])
                break
            else :
                where[index][i.tag] = child

    if len(indices) == 0 :
        if (debug) :
            print 'All search objects empty'
        return

    if debug and verbose:
        print where
    for i in search :
        for index in indices.keys() :
            indices[index].append (where[index][i.tag])
        find_recurse (i, indices)
        for index in indices.keys() :
            indices[index].pop()         

def find_in_pair (pair, out) :
    results = []
    indices = {}
    xml = pair['xml']
    search = pair['search']
    build_index (xml, 1, indices, search.tag)
    if debug:
        print
    find_recurse (search, indices)
    if debug:
        print
    keys = indices.keys()
    keys.sort()
    results.append(str(len(indices)) + '\n')
    for i in keys :
        if debug:
            print str(i) + '\t' + str(indices[i])
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
