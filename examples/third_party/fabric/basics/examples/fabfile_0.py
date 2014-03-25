"""
The simplest of fabfiles.

Two commands: host_type and diskspace.
"""

from fabric.api import run

def host_type():
    run('uname -s')
    
def diskspace():
    run('df')
