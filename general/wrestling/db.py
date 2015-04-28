"""All of our database stuff.
"""

import sqlite3
import os



# Makes/opens database relative to this file.
db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "wrestlers.db3")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()



# When we first init this module, create what we need.
cursor.execute("""CREATE TABLE IF NOT EXISTS wrestlers (
    name text NOT NULL UNIQUE,
    brawn integer,
    finesse integer,
    wins integer,
    losses integer
);""") 
conn.commit()



def cleanup():
    """Call when it's time to close and cleanup the database.
    """
    cursor.close()
    conn.close()



def create_wrestler(**stats):
    """Create a new wrestler in the database.
    """
    try:
        cursor.execute(
            """INSERT INTO wrestlers 
            VALUES ('{0[name]}', {0[brawn]}, {0[finesse]}, {0[wins]}, {0[losses]})
            """.format(stats))
        conn.commit()
    except sqlite3.IntegrityError as err:
        # reraise error so that external things don't need to know about
        # the database error types.
        raise ValueError("Wrestler already exists: %s" % err)



def update_wrestler(**stats):
    """Create a new wrestler in the database.
    """
    try:
        cursor.execute(
            """UPDATE wrestlers SET
            brawn={0[brawn]},
            finesse={0[finesse]}, 
            wins={0[wins]}, 
            losses={0[losses]}
            WHERE name='{0[name]}'
            """.format(stats))
        conn.commit()
    except sqlite3.Error as err:
        # reraise error so that external things don't need to know about
        # the database error types.
        raise ValueError("Something Bad Happened in update_wrestler: %s" % err)



def get_wrestlers():
    """Returns a the raw data of wrestlers as a dictionary.
    """
    results = []
    try:
        cursor.execute("""SELECT * FROM wrestlers""")
        fieldnames = map(lambda x: x[0], cursor.description)
        for wrestler in cursor:
            # Compress with field names and turn into a dictionary
            wrestler = dict(zip(fieldnames, wrestler))
            results.append(wrestler)
    except sqlite3.Error as err:
        print "ERROR in get_wrestlers: %s" % err
    # Make sure we always return a list.
    return results

