# Import our environment. The act of importing will set everything.
import fabenv

from fabric.api import run

def ls():
    # stdout is an extended string type.
    stdout = run('ls -lh /')
    print "exit code of command", stdout.return_code
    print "command succeeded?", stdout.succeeded
    print "command failed?" , stdout.failed
    print "command sent:", stdout.command
    print "command executed:", stdout.real_command
    print "type of command response:", type(stdout)
    print "command response:"
    print stdout
    # It's a string, need to split on lines if we want to iterate or get
    # a line count.
    print "how many lines of output?", len(stdout.splitlines())
