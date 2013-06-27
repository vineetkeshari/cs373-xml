#!/usr/bin/env python

# -------
# imports
# -------

import StringIO
import unittest

from xml.etree import ElementTree as ET
from XML import read_input, read_pairs, build_index, find_recurse, find_in_pair, find_in_pairs, xml_find

# -----------
# TestXML
# -----------

# ----------------
# Test XML strings
# ----------------

# Define strings
# Single pair
string_1 = "<root><one></one><three></three><two></two><four></four></root>\n<one></one>"
string_2 = "<root><one></one><three></three><two></two><four></four></root>\n<three></three>"
string_3 = "<root><one><five></five></one><three><one></one></three><two></two><four><one><five></five></one></four></root>\n<one><five></five></one>"

# Multiple pairs
string_4 = string_1 + string_2
string_5 = string_4 + string_3

# Create test XMLs from strings
test_xml_1 = read_pairs(StringIO.StringIO(string_1))
test_xml_2 = read_pairs(StringIO.StringIO(string_2))
test_xml_3 = read_pairs(StringIO.StringIO(string_3))
test_xml_4 = read_pairs(StringIO.StringIO(string_4))
test_xml_5 = read_pairs(StringIO.StringIO(string_5))

class TestXML (unittest.TestCase) :
    # ---------
    # read_input
    # ---------

    def test_read_1 (self) :
        r = StringIO.StringIO("<root></root>\n")
        b = read_input(r)
        self.assert_(b    == "<root></root>\n")
        
    def test_read_2 (self) :
        r = StringIO.StringIO("<root>\n</root>\n")
        b = read_input(r)
        self.assert_(b    == "<root>\n</root>\n")
        
    def test_read_3 (self) :
        r = StringIO.StringIO("\n<root>\n</root>\n")
        b = read_input(r)
        self.assert_(b    == "\n<root>\n</root>\n")

    def test_read_4 (self) :
        r = StringIO.StringIO("\n")
        b = read_input(r)
        self.assert_(b    == "\n")
               
    def test_read_5 (self) :
        r = StringIO.StringIO("<root></root>\n\n<root></root>")
        b = read_input(r)
        self.assert_(b    == "<root></root>\n\n<root></root>")
                         
    def test_read_6 (self) :
        r = StringIO.StringIO("<root><child/></root>\n\n<root></root>\n<root></root><child></child>")
        b = read_input(r)
        self.assert_(b    == "<root><child/></root>\n\n<root></root>\n<root></root><child></child>")
                         
    # ------------
    # read_pairs
    # ------------

    def test_readpairs_1 (self) :
		r = StringIO.StringIO("<root><one></one><two></two></root>")
		b = read_pairs(r)
		self.assert_(b == [])
		self.assert_(len(b) == 0)

    def test_readpairs_2 (self) :
		r = StringIO.StringIO("<root><one></one><two></two></root>\n<one></one>")
		b = read_pairs(r)
		self.assert_(len(b) == 1)

    def test_readpairs_3 (self) :
		r = StringIO.StringIO("")
		b = read_pairs(r)
		self.assert_(len(b) == 0)

    def test_readpairs_4 (self) :
		r = StringIO.StringIO("<root><child/></root>\n\n<root></root>\n<root></root><child></child>")
		b = read_pairs(r)
		self.assert_(len(b) == 2)

    # -----------
    # build_index
    # -----------

    def test_index_1 (self) :
        test_indices = {}
        build_index(test_xml_1[0]['xml'], 1, test_indices, "ten")
        self.assert_(test_indices == {})
		
    def test_index_2 (self):
        test_indices = {}
        build_index(test_xml_2[0]['xml'], 1, test_indices, "three")
        self.assert_(test_indices.keys() == [3])

    def test_index_3 (self):
        test_indices = {}
        build_index(test_xml_3[0]['xml'], 1, test_indices, "one")
        self.assert_(test_indices.keys() == [8, 2, 5])

    # -----------
    # find_recurse
    # ------------
    
    def test_find_recurse_1 (self):
        test_indices = {}
        build_index(test_xml_1[0]['xml'], 1, test_indices, "ten")
        find_recurse(test_xml_1[0]['search'], test_indices)
        self.assert_(test_indices == {})
	
		
    def test_find_recurse_2 (self):
        test_indices = {}
        build_index(test_xml_2[0]['xml'], 1, test_indices, "three")
        find_recurse(test_xml_2[0]['search'], test_indices)
    	self.assert_(test_indices.keys() == [3]) # Finds the pattern at index 3

    def test_find_recurse_3 (self):
    	test_indices = {}
    	build_index(test_xml_3[0]['xml'], 1, test_indices, "one")
        find_recurse(test_xml_3[0]['search'], test_indices)
    	self.assert_(test_indices.keys() == [8, 2]) # Finds the pattern at indices 8 and 2
    		
    # -----------
    # find_in_pair
    # -----------
    
    def test_find_in_pair_1 (self):
        results = []
        find_in_pair(test_xml_1[0], results)
        self.assert_(results == ['1\n', '2\n'])

    def test_find_in_pair_2 (self):
        results = []
    	find_in_pair(test_xml_2[0], results)
    	self.assert_(results == ['1\n', '3\n'])

    def test_find_in_pair_3 (self):
    	results = []
    	find_in_pair(test_xml_3[0], results)
    	self.assert_(results == ['2\n', '2\n', '8\n'])
    	    	
    # -------------
    # find_in_pairs
    # -------------
    
    def test_find_in_pairs_1 (self):
        results = []
        find_in_pairs(test_xml_1, results)
        self.assert_(results == ['1\n', '2\n'])

    def test_find_in_pairs_2 (self):
        results = []
    	find_in_pairs(test_xml_2, results)
    	self.assert_(results == ['1\n', '3\n'])

    def test_find_in_pairs_3 (self):
    	results = []
    	find_in_pairs(test_xml_3, results)
    	self.assert_(results == ['2\n', '2\n', '8\n'])

    def test_find_in_pairs_4 (self):
    	results = []
    	find_in_pairs(test_xml_4, results)
    	self.assert_(results == ['1\n', '2\n', '\n', '1\n', '3\n'])

    def test_find_in_pairs_5 (self):
    	results = []
    	find_in_pairs(test_xml_5, results)
    	self.assert_(results == ['1\n', '2\n', '\n', '1\n', '3\n', '\n', '2\n', '2\n', '8\n'])
    
    # -----------
    # xml_find
    # -----------

    def test_xml_find_1 (self):
    	r = StringIO.StringIO(string_1)
    	w = StringIO.StringIO()
    	xml_find(r, w)    	
    	self.assert_( w.getvalue() == '1\n2\n' )

    def test_xml_find_2 (self):
    	r = StringIO.StringIO(string_2)
    	w = StringIO.StringIO()
    	xml_find(r, w)
    	self.assert_( w.getvalue() == '1\n3\n' )

    def test_xml_find_3 (self):
    	r = StringIO.StringIO(string_3)
    	w = StringIO.StringIO()
    	xml_find(r, w)
    	self.assert_( w.getvalue() == '2\n2\n8\n' )

    def test_xml_find_4 (self):
    	r = StringIO.StringIO(string_4)
    	w = StringIO.StringIO()
    	xml_find(r, w)
    	self.assert_( w.getvalue() == '1\n2\n\n1\n3\n' )

    def test_xml_find_5 (self):
    	r = StringIO.StringIO(string_5)
    	w = StringIO.StringIO()
    	xml_find(r, w)
    	self.assert_( w.getvalue() == '1\n2\n\n1\n3\n\n2\n2\n8\n' )

# ----
# main
# ----

print "TestXML.py (contains 29 tests for 7 functions)"
unittest.main()
print "Done."
