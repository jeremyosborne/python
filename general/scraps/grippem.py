
import os
import grip
from fnmatch import fnmatch

def grippem(path, username=None, password=None):
    """Recurse through folders, find .md files, run grip on them.

    Requires [grip](https://github.com/joeyespo/grip).
    """
    at_least_one = False
    print "grippem walking through:", path
    walker = os.walk(path)
    for cwd in walker:
        for f in cwd[2]:
            f = os.path.realpath(os.path.join(path, cwd[0], f))
            if fnmatch(f, "*.md"):
                at_least_one = True
                print "markdown file found:", f
                grip.export(f, gfm=True, username=username, password=password)
    
    if at_least_one is not True:
        print "No markdown files found."
        
if __name__ == "__main__":
    grippem(os.path.realpath(os.path.dirname(__file__)))
