#!/usr/bin/env python
"""Export a github repo or a portion of it.

Makes git act like svn export (since github doesn't seem to like
git archive).
"""

import getpass
import sys
import os
import shlex
from subprocess import check_output


def github_export(user, project, branch="master", path="", localname=""):
    """Attempts to export a repo, folder, or file from github.

    Uses check_output and will raise equivalent errors if the command
    fails.
    """
    CMD_TEMPLATE = "svn export https://github.com/%(user)s/%(project)s/%(branch)s/%(path)s %(localname)s"

    # Mappings, likely only one, for translating github to svn.
    GITHUB_BRANCH_MAPPINGS = { "master": "trunk" }

    if branch in GITHUB_BRANCH_MAPPINGS:
        branch = GITHUB_BRANCH_MAPPINGS[branch]

    cmd_context = { 
            "user": user,
            "project": project,
            "branch": branch,
            "path": path,
            "localname": localname
            }

    cmd = CMD_TEMPLATE % cmd_context
    #print "Attempting to", cmd
    check_output(shlex.split(cmd))



def main():
    context = {}
    # If set, will not ask for username.
    GITHUB_DEFAULT_USER = "jeremyosborne" #or getpass.getuser()

    # Default branch.
    GITHUB_DEFAULT_BRANCH = "master"

    # Path where script is located is where projects will be mirrored.
    SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))

    # Indenting.
    print "\nGithub export (for projects, folders, or files)."
    print "Script running in:", SCRIPT_DIR

    user = raw_input("Github user [%s]:" % GITHUB_DEFAULT_USER)
    if not user:
        user = GITHUB_DEFAULT_USER
    context["user"] = user

    project = raw_input("Project: ")
    if not project:
        print "Sorry, need a project. Exiting."
        sys.exit(1)
    context["project"] = project

    branch = raw_input("Branch [%s]: " % GITHUB_DEFAULT_BRANCH)
    if not branch:
        branch = GITHUB_DEFAULT_BRANCH
    context["branch"] = branch

    path = raw_input("Path to specific folder or file to export [optional]: ")
    if path:
        context["path"] = path

    localname = raw_input("Local renaming [optional]: ")
    if localname:
        context["localname"] = localname

    try:
        github_export(**context)
    except Exception as err:
        print "Problem with export:", err
        sys.exit(1)

    print "Export seems to have worked."



if __name__ == "__main__":
    main()

