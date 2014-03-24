"""Lab:

* Grab all of the links from a web page.
* Make a list of links in a simple HTML file.
* Make sure the links work.

Requirements:

    pip install beautifulsoup4
    pip install requests

"""

import requests
from bs4 import BeautifulSoup
from io import StringIO
import re

domain = 'http://gog.com/'

html = requests.get(domain).text
soup = BeautifulSoup(html)

page_template = """<!DOCTYPE html>
<html lang='en-US'>
    <head>
        <meta charset="UTF-8"/>
        <title>Some links</title>
    </head>
    <body>
        <h1>List of links from: {}</h1>
        <ul>
        {{}}
        </ul>
    </body>
</html>
""".format(domain)

links = StringIO()
link_template = "<li><a href='{0}{1[href]}'>{1.text}</a></li>\n"
for link in soup.find_all('a'):
    href = link.get("href")
    if not href:
        # Might be a named anchor.
        continue
    linkdomain = re.match(r"\/\/|http:\/\/|https:\/\/", href)
    if linkdomain:
        # External link, don't correct.
        linkdomain = ""
    else:
        # Relative link, make accessible from our page.
        linkdomain = domain
    links.write(unicode(link_template.format(linkdomain, link)))

with open("links.html", "w") as f:
    f.write(page_template.format(links.getvalue()))

