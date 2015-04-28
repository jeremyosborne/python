# Parsing of URLs
#
# scheme://netloc/path;params?query#fragment

import urllib
import urlparse

url = "http://example.com:8080/hello/world;matrix=thisis?q=1&q=2&cb=func#page1"
u = urlparse.urlparse(url)
print u
# We can access each piece
print u.scheme
print u.netloc
print u.hostname
print u.port
print u.path
print u.params
print u.query
print u.fragment

# Parse out a URL query string.
print urlparse.parse_qs(u.query)

# NOTE: read only, can't change things as is...
#u.port = 80

#...however
modu = list(u)

print modu
# change the query string
qs = {"dogs": "cats", "chickens": "wie geht's?"}
# use to encode the query string back together
modu[4] = urllib.urlencode(qs)


# back to a string format, compare the two.
print urlparse.urlunparse(u)
print urlparse.urlunparse(modu)

