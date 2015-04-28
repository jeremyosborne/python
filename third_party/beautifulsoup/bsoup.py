"""BeautifulSoup document parser/page scraper.

Requires:

    pip install beautifulsoup4
    pip install requests

"""

import requests
from bs4 import BeautifulSoup

html = requests.get('http://gog.com/').text

soup = BeautifulSoup(html)

print "\nCleaned up content:\n%s" % soup.prettify() 
print "\nContent of the <title> tag:\n%s" % soup.title
print "\nContent of the <body> tag:\n%s" % soup.body

print "\nLinks from this page and where they are going:"
anchors = soup.find_all('a')
for anchor in anchors:
    print "%40s href to -> %s" % (anchor.text, anchor.get("href") or "N/A (no href)")

print "\nAny imported scripts?"
scripts = soup.find_all('script')
for script in scripts:
    try:
        print "%40s href to -> %s" % (script.text, script["src"])
    except KeyError:
        print "Script without src, must be an inline script."
        print "Contents of inline script:"
        print script.text

print "\nIs this document in a certain encoding?"
try:
    print "\tYes, it is: %s" % soup.find(lambda el: el.has_attr('charset'))["charset"]
except:
    print "\tNo language declared for this document."

