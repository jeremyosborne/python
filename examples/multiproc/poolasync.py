from multiprocessing import Pool
import time

def finite(myid, iters=0):
    results = ["(id %s): start time is: %s" % (myid, time.time())]
    for i in xrange(iters):
        pass
    results.append("(id %s): end time is: %s" % (myid, time.time()))
    # What gets resturned gets caught by apply_async and passed to
    # callback.
    return results
    
def done(results):
    print "We got the following results:"
    print "\n".join(results)

if __name__ == '__main__':
    pool = Pool(processes=1)
    result = pool.apply_async(finite, 
                              args=(100,),
                              kwds={"iters":10000000},
                              callback=done)
    print "Will see before the results..."
    result.wait()
    # Could also do the following instead of the callback.
    #print result.get()
