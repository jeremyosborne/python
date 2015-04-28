# This example reviews the basic Python DB-API
# but uses the sqlite database as an example.
# The DB-API in Python is formally defined in
# http://www.python.org/dev/peps/pep-0249/
# (which translates to Python Enhancement Proposals #249)
# Even though we're using sqlite3, the DB APIs in Python operate
# like this.

# Use the sqlite3 api, which is part of the standard lib.
import sqlite3
# In sqlite-isms, this will create a local file named sample.
# We can also use the special keyword ":memory:" to create an in memory
# database.
conn = sqlite3.connect(':memory:')
#conn = sqlite3.connect("sample.db3")

# Create a cursor object that is used to execute commands
c = conn.cursor()

# Run a single query.
# The best way to run queries is to watch them.
try:
    c.execute('''create table if not exists rolls (value integer, count integer)''')
except sqlite3.Error as err:
    print "Problem with sqlite3:", err


# Insert data in the db.
c.execute("""insert into rolls values (2, 1)""")


# When we're done with our connection and cursor.
conn.commit()
# Could also conn.rollback() any changes since the last commit.

# For multiple inserts or updates:
for r in [(2, 1),
          (7, 5),
          (12, 1),
         ]:
    c.execute('insert into rolls values (?,?)', r)

# or

data = [
    (2, 1),
    (3, 5),
    (5, 5),
    (7, 20),
    (12, 1),
]
c.executemany('insert into rolls values (?, ?)', data)

# Get data from the database.
c.execute('select * from rolls')
# When performing a select, the .description property will be available on
# the cursor.
print c.description
# Note that this is hardly readable in with all the nulls. We can make this
# more readable with a simple:
print map(lambda x: x[0], c.description)
# One way of interacting with the table rows that come back
# since the cursor acts as an iterable recordset.
for row in c:
    print row
    
# A trick to return the results of a select as a list of dictionary objects
# vs. a tuple
c.execute('select * from rolls')
output = []
labels = map(lambda x: x[0], c.description)
for row in c:
    row = dict(zip(labels, row))
    output.append(row)
# view the list of dictionaries
print output
    


# NOTE: While rowcount works for update and delete usually as expected,
# rowcount for select statements cannot be relied upon, even with sqlite3
# BECAUSE the total number of rows of a select statement is usually never
# determined because the data is rarely fully retrieved from the databse
# until the last row is actually retrieved.

# Test to see if something was updated correctly
c.execute("update rolls set count=1 where value=7")
if c.rowcount > 0:
    print "%s rows updated" % c.rowcount
else:
    print "Nothing updated."

# Update the db.
conn.commit()

# Multiple commands can be run with an execute script command.
c.executescript("""
    delete from rolls where count=2;
    delete from rolls where count=3;
""")

# Update the db.
conn.commit()


