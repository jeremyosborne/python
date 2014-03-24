import os
import re

def findfiles(path, ext=".pyc"):
    """ Returns a list of all files of an extension in a path.

    @param path {str} Initial path to the directory we
    want to crawl.
    @param [ext=".pyc"] {str} what file extensions to look for. This is
    a literal match and must contain the dot.
    """
    results = []
    regex = re.compile(re.escape(ext)+"$", re.I)

    tree = os.walk(path)
    for d in tree:
        # Each element of a walker represents a directory and its contents.
        # Diagnostic, if you wish.
        #print(d)
        if d[2]:
            # Are there files in this directory?
            for f in d[2]:
                if regex.findall(f):
                    relpath = os.path.join(d[0], f)
                    results.append(os.path.realpath(relpath))

    return results



if __name__ == "__main__":
    for path in findfiles("../"):
        print "File found:", path
        # If the user is feeling brave, they can use:
        if raw_input("Do you wish to delete this file? ").lower() == "y":
            print "Removing file:", path
            # Uncomment if you really want to remove the file.
            #os.remove(path)
