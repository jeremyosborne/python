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


