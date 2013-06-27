all:
	make XML.zip

clean:
	rm -f RunXML.tmp
	rm -f XML.html
	rm -f XML.log
	rm -f XML.zip
	rm -f *.pyc

diff: RunXML.in RunXML.out RunXML.py
	RunXML.py < RunXML.in > RunXML.tmp
	diff RunXML.out RunXML.tmp
	rm RunXML.tmp

turnin-list:
	turnin --list eladlieb cs373pj1

turnin-submit: XML.zip
	turnin --submit eladlieb cs373pj1 XML.zip

turnin-verify:
	turnin --verify eladlieb cs373pj1

XML.html: XML.py
	pydoc -w XML

XML.log:
	git log > XML.log

XML.zip: XML.html XML.log XML.py RunXML.in RunXML.out RunXML.py SphereXML.py TestXML.py TestXML.out
	zip -r XML.zip  XML.html XML.log XML.py RunXML.in RunXML.out RunXML.py SphereXML.py TestXML.py TestXML.out

RunXML.out: RunXML.in RunXML.py
	RunXML.py < RunXML.in > RunXML.out

TestXML.out: TestXML.py
	TestXML.py > TestXML.out 2>> TestXML.out
