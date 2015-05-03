#!/usr/bin/env python
"""Clone github repos locally.

Logic of script:

* Pull down list of github repos using provided credentials.
* If repo names do not match local folder on disk, clone the repo.
* If repo name matches directory name on disk, do not update.

Script should be run from where you want to put the repos.

    cd directory/of/all/repos
    python git_backup.py
    # Fill in prompt information.

"""

import requests
import getpass
import sys
import os
from subprocess import check_output



# Git mirror template
GIT_MIRROR = "git clone git://github.com/%(user)s/%(project)s.git %(project)s"

# Auth determines list of repos.
GITHUB_REPO_API = 'https://api.github.com/user/repos'

# If set, will not ask for username.
GITHUB_DEFAULT_USER = "jeremyosborne"

# Path where script is located is where projects will be mirrored.
SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))

# Indenting.
INDENT = "  "

def get_repos(user, password):
    res = requests.get(GITHUB_REPO_API, auth=(user, password))
    if res.status_code >= 400:
        msg = res.json().get('message', 'UNDEFINED ERROR (no error description from server)')
        raise Exception(msg)
    else:
        # Return names mapped with user.
        return map(lambda r: {"project": r["name"], "user": user}, res.json())



print "\nMirroring remote github repos."
print "Script running in:", SCRIPT_DIR

user = GITHUB_DEFAULT_USER or getpass.getuser()
if not user:
    user = raw_input("Github user: " % user)

password = getpass.getpass("Github user password (for user %s): " % user)
if not password:
    print "Sorry, need a password."
    sys.exit(1)

try:
    repos = get_repos(user, password)
except Exception as err:
    print "Problem retrieving repo list from github:"
    print err
    sys.exit(1)
    
print "\nRepos found:"
for r in repos:
    print "%s%s" % (INDENT, r["project"])
    if os.path.exists(os.path.join(SCRIPT_DIR, r["project"])):
        print "%salready exists, skipping." % (INDENT*2)
    else:
        print "%sdoesn't exist, mirroring." % (INDENT*2)
        try:
            print "Attempting to clone with:", GIT_MIRROR % r
            check_output(GIT_MIRROR % r, shell=True)
        except Exception as err:
            print "%sSorry, could not mirror repo." % (INDENT*2)
            print "%s%s" % (INDENT*2, err)
        else:
            print "%sSUCCESS" % (INDENT*2)



