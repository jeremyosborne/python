


import urllib
import urllib2

from urlparse import urlparse


# Sample url. See: http://ivanzuzak.info/urlecho/
url = "http://urlecho.appspot.com/echo"
# Query string, specific to the 
data = urllib.urlencode({"status": 200,
                          "Content-Type": "text/plain",
                          "body": "Yes, sir!"})



# GET, by nature of passing data.
# Get and post will return different content by nature of the remote API.
try:
    get_url = "%s?%s" % (url, data)
    print "Making get request to:", get_url
    response = urllib2.urlopen(get_url)
    # See the url we worked with.
    print "Response from:", response.geturl()
    print "Response from hostname:", urlparse(response.geturl()).hostname
    print "Status code:", response.getcode()

    print "Response headers:"
    for name, value in response.info().items():
        print "{}: {}".format(name, value)
    
    print "Response content:\n", response.read()

except urllib2.HTTPError as err:
    print "Request to %s failed with %s and reason %s." % (url, err.code, err.reason)
    


# POST, by nature of passing data.
try:
    print "Making post request to:", url
    response = urllib2.urlopen(url, data)
    # See the url we worked with.
    print "Response from:", response.geturl()
    print "Response from hostname:", urlparse(response.geturl()).hostname
    print "Status code:", response.getcode()

    print "Response headers:"
    for name, value in response.info().items():
        print "{}: {}".format(name, value)
    
    print "Response content:\n", response.read()

except urllib2.HTTPError as err:
    print "Request to %s failed with %s and reason %s." % (url, err.code, err.reason)
    
