import os

from fabric.api import run
from fabric.api import env

# Where is this file located at?
cwd = os.path.realpath(os.path.dirname(__file__))

# whoami
env.user = "student1"
# List of hosts to run against.
env.hosts = [
    'ec2-75-101-223-215.compute-1.amazonaws.com',
]
# Location of our keyfile.
env.key_filename = os.path.join(cwd, "..", "student")

def host_type():
    run('uname -s')
    
def diskspace():
    run('df')
