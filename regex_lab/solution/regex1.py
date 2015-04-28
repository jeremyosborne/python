# Find the IP address in the following line using a regex group and the
# re.search function. Print the IP address using the match object group
# method, as well as the index of where the grouping starts and ends.
log = '208.115.111.73 - - [01/Apr/2013:06:30:26 -0700] "GET /nanowiki/index.php/1_November_2007_-_Day_1 HTTP/1.1" 404 36 "-" "Mozilla/5.0 (compatible; Ezooms/1.0; ezooms.bot@gmail.com)"'
import re
pattern = r"^(\d+\.\d+\.\d+\.\d+)\b"
match = re.search(pattern, log)
print "IP: {} (first index: {}, last index: {})".format(match.group(1), match.start(1), match.end(1))
