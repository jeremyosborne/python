# Import our environment. The act of importing will set everything.
import fabenv

from fabric.api import run

def host_type():
    run('uname -s')
    
def diskspace():
    run('df')
