#!/usr/bin/env python
'''
Lab - Average Uptime

Write a script that uses the Fabric library to poll a group of hosts for their
uptimes, and displays their average uptime for the user.
'''


from fabric import tasks
from fabric.api import run
from fabric.api import env
from fabric.network import disconnect_all


# Creates a set of simulated hosts.
env.hosts = ["test1", "test2", "test3", "test4", "test5",]
    
