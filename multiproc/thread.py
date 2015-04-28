# Why potentially use multiprocessing over threading?
# See:
#
#     http://eli.thegreenplace.net/2012/01/16/python-parallelizing-cpu-bound-tasks-with-multiprocessing/
#     and
#     http://www.dabeaz.com/GIL/


import threading

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
        print 'My name is {0}!'.format(self.name)

def worker(obj):
    obj.speak()

if __name__ == '__main__':
    name = "George Foreman %s"
    
    threads = []
    for i in range(10):
        # Fill the qs
        t = threading.Thread(target=worker, args=(NamedObject(name % i),))
        t.start()
        threads.append(t)
    
# Optional, should we wish to block for results.
#     for t in threads:
#         t.join()

