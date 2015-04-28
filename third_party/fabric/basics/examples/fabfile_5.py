import time
import os

from fabric import tasks
from fabric.api import parallel, run, env
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


# Manage N number of connections in parallel, max.
@parallel(pool_size=3)
def time_to_echo():
    """A command that can run across multiple hosts in parallel.
    
    Returns the amount of time necessary to begin or end the command.
    """
    # Rough timing of the command.
    begin = time.time()
    run("echo hello world", quiet=True)
    end = time.time()
    return end - begin
        


# We want to run this as a python function. This is not a Fabric
# task.
def main_task():
    # run the "time_to_echo" task once for each host, respecting
    # decorators.
    results = tasks.execute(time_to_echo)
    print "Total number of hosts queried:", len(results)
    print "Hosts queried:"
    # results is a dictionary.
    for host in results:
        print "   ",host
    print "Total time to execute requests:", sum(results.values())
    # We're supposed to call this when done.
    disconnect_all() 



if __name__ == "__main__":
    main_task()
