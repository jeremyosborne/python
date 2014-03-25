#!/usr/bin/env python
'''
Lab - Average Uptime

Write a script that uses the Fabric library to poll a group of hosts for their
uptimes, and displays their average uptime for the user.
'''

import os

from fabric import tasks
from fabric.api import run
from fabric.api import env
from fabric.api import parallel
from fabric.network import disconnect_all

# Assumed working directory.
wd = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
# TODO: Replace with the user you are using.
env.user = "student1"
# TODO: Replace with the location of your keyfile, if it is different.
env.key_filename = os.path.join(wd, "student")
# TODO: Replace the HostName placeholders with the test hostname in the
# associated ssh_config file.
env.use_ssh_config = True
env.ssh_config_path = os.path.join(wd, "examples", "ssh_config")
# Creates a set of simulated hosts.
env.hosts = ["test1", "test2", "test3", "test4", "test5",]



@parallel
def uptime():
    res = run('cat /proc/uptime')
    try:
        seconds = float(res.split(' ')[0])
    except:
        print "Oops, bad response from server!"
        print res
        return 0
    return seconds



def main():
    uptimes = tasks.execute(uptime)
    avg_ut = sum(uptimes.values()) / len(uptimes)
    print '-' * 80
    print
    print 'Average Uptime: %s' % avg_ut
    print
    print '-' * 80
    disconnect_all()



if __name__ == '__main__':
    main()
    