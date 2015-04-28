"""Log file parsing.

Parse the data/access.log.

Use re module and build a regular expression that will return the ip of each
log entry.
Using map, iterate the file line by line and parse out the ip of each access.
Display the total number of acccesss.
Use collections.Counter to determine the top 10 unique accesses.
Print out the top 10 unique accesses.
Using io (BytesIO) and csv, write an in memory CSV file in a buffer.
Using gzip, save the CSV file in memory to disk as a gzipped CSV file.
"""



import re
from collections import Counter
import io
import csv
import gzip



# Probably not robust enough for all log files....
pattern = r'([\d\.]+|[:\d]+) - - \[(.*?)\] "(.*?)" (\d+|-) (\d+|-)'
regex = re.compile(pattern)



with open("../data/access.log") as f:
    accesses = map(lambda line: regex.match(line).groups()[0], f)

print "Number of log entrys:", len(accesses)



# Our wellformed log entries can be counted.
print "Top 10 ips accessing our server."
top10 = Counter(accesses).most_common(10)
for ip, count in top10:
    print ip, count



# The csv module does not like UTF8. It's technically binary.
fbuffer = io.BytesIO()
csvwriter = csv.writer(fbuffer)
csvwriter.writerows(top10)
# Deflate (maximum compression) the CSV and write to a file.
gz = gzip.open('top10.csv.gz', 'wb')
gz.write(fbuffer.getvalue())
gz.close()
