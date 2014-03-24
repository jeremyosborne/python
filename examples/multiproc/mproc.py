# Why potentially use multiprocessing over threading?
# See:
#
#     http://eli.thegreenplace.net/2012/01/16/python-parallelizing-cpu-bound-tasks-with-multiprocessing/
#     and
#     http://www.dabeaz.com/GIL/


# Notes about multiprocessing: Need to be able to do multiple imports on
# the __main__ file, and as such cannot do these examples from the command
# line.
import multiprocessing

import time
import random

class NamedObject(object):
    """Object identifiable by a name.
    """
    def __init__(self, name):
        self.name = name
    def speak(self):
        # arbitrary minor pause.
        time.sleep(random.random())
        # Processes have names. We can get the name from the multiprocess
        # module static method current_process. The name is arbitrary.
        proc_name = multiprocessing.current_process().name
        print 'My name is {0}, and I am in {1}!'.format(self.name, proc_name)


def worker(q):
    while q.empty() is not True:
        # Pull an item from the queue.
        obj = q.get()
        # We assume that we're only getting NamedObjects.
        # If we weren't getting named objects, this would break.
        obj.speak()

if __name__ == '__main__':
    name = "George Foreman %s"
    
    # Queues are First In, First Out objects designed for passing data into
    # a process callback.
    qs = multiprocessing.Queue(), multiprocessing.Queue()
    
    for i in range(10):
        # Fill the qs
        qs[i % 2].put(NamedObject(name % i))
    
    # This spawns our secondary process.
    # Should always call with keyword arguments.
    # target is our callback function
    # args {tuple} are passed to our target as formal arguments.
    p = multiprocessing.Process(target=worker, args=(qs[0],))
    p2 = multiprocessing.Process(target=worker, args=(qs[1],))
    # Begin the process.
    p.start()    
    p2.start()
    
    # Attempt to join the background process and flush the queue into it.
    # But, if we close, we don't have to purposefully join.
    # (This call is not always required, it is implied when we call close and
    # the process is not a daemon).
    #qs[0].join_thread()
    #qs[1].join_thread()

    # Wait for the worker to finish
    # Close indicates no more data will be added to the queue.
    # We need to close the data queue before joining the thread.
    qs[0].close()
    qs[1].close()
    
    # Pause until the process terminates (blocking call).
    # (This call is not required).
    #p.join()
    #p2.join()
    
    # With the join call, print will not execute until the queue is empty.
    # Turn off the p.join() above and print will call before the other procs.
    print "If join is called, I will always be last. If not...."
