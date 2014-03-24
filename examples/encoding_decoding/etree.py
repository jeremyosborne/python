# NOTE 1: XML parsing isn't any _easier_ in Python.
# NOTE 2: we need to use the example.xml file in the testdocs folder
# in the class folder.
#
# For a list of the limited XPath that ElementTree supports:
# http://effbot.org/zone/element-xpath.htm

import xml.etree.ElementTree as etree
# Loads XML from a string (useful for responses to requests).
# Returns an Element type, which is similar to a full ElementTree.
# ASSUMES: that we have the example.xml file available.
f = open('data/example.xml', "r")
xml_string = f.read()
f.close()
xml = etree.fromstring(xml_string)
print type(xml)
# Get the tag of the element
print xml.tag
# Get the opening content of the XML
# NOTE: world is missing
print xml.text 
# Get the attributes.
# NOTE: this is a read/write dictionary
print xml.attrib
# set the lang value
xml.attrib["lang"] = "en"
# xpath, which is very, very limited in the etree module
found = xml.find("body")
print found.tag

p = xml.find("body/p")     
print p
# <Element 'p' at 0xb77ec26c>
# How many children?
print len(p)
# 2
# Fragment text of paragraph
print p.text
print dir(p[0])
# Shows stuff
print p[0].attrib.keys()
# ['href']
# Content of first child
print p[0].text
# 'example.org'
# Ways of returning a list of all links
links = p.findall("a")
# reminder: find only returns the first match of the xpath query, so we use
# findall above
# or, or we could use
links = list(p)
print links
# [<Element 'a' at 0xb77ec2ac>, <Element 'a' at 0xb77ec1cc>]
# Iterates through all found links
for i in p:
    i.attrib["target"] = "blank"



# If we want to append a new element to an existing structure
newlink = etree.Element("a", {"href":"http://test.com"})
# Need to make the element a subelement of an existing element
p = xml.find("body/p")
p.append(newlink)
# Or we could insert it at a specific index.
p.insert(0, newlink)

# output XML back to a string doc
f = open("output.html", "w")
f.write (etree.tostring(xml))
f.close()

# Different ways of outputting an ElementTree
# or we can write out the tree to sys.stdout
# tree.write(sys.stdout)
# or another way to dump to standard out
# etree.dump(tree)
# or if we want it as a string, we need to grab the root element
# etree.tostring(tree.getroot())
# or we can write out the tree to a file
# tree.write("output.xml")

# Take a look at the new file
