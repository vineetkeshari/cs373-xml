#!/lusr/bin/python

from xml.etree import ElementTree as ET

# Use these to print debug information
debug = False
verbose = False

def read_input (r) :
    """
    Reads a string from StringIO

    r : input StringIO object
    xml : string read from r
    """
    assert not r is None

    xml = ''
    while True :
        read = r.readline()
        if read == '' :
            break
        assert not read == ''
        xml = xml + read

    return xml

def read_pairs (r) :
    """
    Parses all {XML, SearchXML} pairs from a string

    r : input string containing XMLs
    pairs : List of {XML, SearchXML} pairs.
      Each pair is a dict with keys 'xml' and 'search'
    """
    xml = read_input (r)
    if (debug) :
        print xml

    # Wrap all XMLs in sentinel tags so that ET can read all of them together
    root = ET.fromstring("<PAIRS>" + xml + "</PAIRS>")
    assert type(root) is ET.Element

    # Create XML and SearchXML pairs by taking two XMLs at a time from root
    # If odd no. of XMLs, ignore last one
    pairs = []
    for index in range(0,len(root),2) :
        if index+1 == len(root) :
            break

        assert index+1 < len(root)
        pairs.append ({'xml': root[index], 'search': root[index+1]})

    return pairs

def build_index (xml, xml_index, indices, search_root_tag) :
    """
    Indexes all tags in XML and stores tags matching search XML root tag

    xml : Node in XML
    xml_index : Index of node 'xml'
      Nodes are indexed in the order they appear in the XML
    indices : Stores all possible matches to search XML (search object)
      If the node's tag matches that of the search XML root,
      it is a possible match to the search XML
    search_root_tag : Tag of the root of the search XML
    """
    if (debug):
        print str(xml_index) + '\t' + xml.tag

    assert xml_index > 0
    assert not xml.tag == ''
    assert type(indices) is dict

    # Add search object to indices as a possible match if tag is same as search root
    if xml.tag == search_root_tag :
        indices[xml_index] = [xml]

    # For first child, index is one more that self
    # For all other children, index is one more than
    # the largest index assigned in recursive call to previous child
    for child in xml :
        xml_index = build_index (child, xml_index+1, indices, search_root_tag)

    assert xml_index > 0
    return xml_index

def find_recurse (search, indices) :
    """
    Recurses through search XML, comparing each child with
    the children of possible matches stored in indices

    search : Current node in the search XML
    indices : Dict of all possible matches
      All non-matching nodes in XML are removed from indices
      if the children do not match at any step during recursion
    """
    assert type(indices) is dict
    assert not search.tag == ''
    if (debug) :
        print search.tag
        if (verbose) :
            print indices

    for index in indices.keys() :
        if (debug) :
            print str(index) + '\t' + str(indices[index])
        assert len(indices[index]) > 0

        # The node to be compared is the top-most one in each search object's stack
        node = indices[index][-1]
        assert not node.tag == ''

        # If tags don't match, remove the search object at index
        if not search.tag == node.tag :
            if (debug):
                print '[F] Unequal'
            del(indices[index])
            assert not index in indices
            continue

        # If there are more children in the search XML's node,
        # there cannot be a match. So, remove this search object
        if len(search) > len(node) :
            if (debug) :
                print '[F] Search node has more children at ' + str(index)
            del(indices[index])
            assert not index in indices
    
    # No children in search node? This means we have a match.
    if len(search) == 0 :
        if (debug) :
            print 'Lowest level!'
        return

    # Terminate recursive calls if all search objects deleted
    # as no possible matching node remains.
    if len(indices) == 0 :
        if (debug) :
            print 'All search objects empty'
        return

    assert len(search) > 0
    assert len(indices) > 0

    # where stores the location of each child in each XML node in indices
    # for quick access when making the next level of recursive calls
    where = {}

    for index in indices.keys() :
        assert type(where) is dict
        where[index] = {}
        node = indices[index][-1]

        for i in search :
            assert not i.tag == ''
            assert type(where[index]) is dict
            
            # ElementTree's find method returns the first matching child
            # Since all siblings are unique, we only need to find once.
            child = node.find (i.tag)

            # Remove the search object from indices and break
            # even if a single child is not found
            if child == None :
                if (debug) :
                    print '[F] %s not found at %d' % (i.tag, index)

                del(indices[index])
                del(where[index])
                assert not index in indices
                assert not index in where

                break
            else :
                where[index][i.tag] = child

    # We check for this each time indices has possibly been emptied
    if len(indices) == 0 :
        if (debug) :
            print 'All search objects empty'
        return

    assert len(indices) > 0
    if debug and verbose:
        print where

    # At this stage, indices only contains the search objects that are
    # still valid, so compare the children in search XML recursively
    # with the contents of 'where' assigned above.
    for i in search :

        # Push and pop the appropriate elements in 'where' before and after
        # the recursive calls respectively.
        for index in indices.keys() :
            assert type(indices[index]) is list
            indices[index].append (where[index][i.tag])

        find_recurse (i, indices)

        for index in indices.keys() :
            indices[index].pop()         

def find_in_pair (pair, out) :
    """
    Finds all instances of 'search' in 'xml' for a pair of XMLs

    pair : Dict containing an XML and a search XML
    out : List containing each line of the output for this pair
    """
    results = []
    indices = {}

    assert 'xml' in pair
    assert 'search' in pair
    xml = pair['xml']
    search = pair['search']

    assert type(xml) is ET.Element
    assert type(search) is ET.Element
    assert not search.tag == ''
    
    # First, we build the index and store all search objects
    build_index (xml, 1, indices, search.tag)

    # Now, compare each search object with the search XML
    # by recursing through each at the same time
    if debug:
        print
    assert type(indices) is dict
    find_recurse (search, indices)
    if debug:
        print

    # 'indices' will contain all nodes in XML that match the search XML.
    # Generate output as a list of lines
    keys = indices.keys()
    keys.sort()
    results.append(str(len(indices)) + '\n')

    for i in keys :
        if debug:
            print str(i) + '\t' + str(indices[i])
        results.append (str(i) + '\n')

    # Append new output to out
    assert type(out) is list
    out.extend (results)

def find_in_pairs (pairs, out) :
    """
    Finds matches for all pairs of XML and search XML

    pairs : List containing all pairs
    out : List of lines in output
    """
    assert type(pairs) is list

    for pair in pairs :
        find_in_pair (pair, out)

        assert type(out) is list
        out.append('\n')

    # Pop the last newline
    out.pop()

def xml_find (r, w) :
    """
    Finds matches in the input stream and writes the results to output stream

    r : Input stream containing several XMLs
    w : Output stream the result of all matches is written to
    """
    assert not r is None
    assert not w is None

    # Read the pairs
    pairs = read_pairs (r)

    # Match all pairs
    result = []
    assert type(pairs) is list
    find_in_pairs (pairs, result)

    # Output the results
    w.writelines (result)
