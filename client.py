import multiprocessing
from multiprocessing.managers import SyncManager
import time
import Queue

import tasks

IP="127.0.0.1"
PORTNUM=1337
AUTHKEY = "asdf"

def factorize_naive(n):
    """
    TODO: Put work here
    """
    if n < 2:
        return []
    
    factors = []
    p = 2

    while True:
        if n == 1:
            return "Woop"
            #return factors

        r = n % p
        if r == 0:
            factors.append(p)
            n = n / p
        elif p * p >= n:
            factors.append(n)
            return factors
        elif p > 2:
            # Advance in steps of 2 over odd numbers
            p += 2
        else:
            # If p == 2, get to 3
            p += 1
    return "Woo"

def factorizer_worker(job_q, result_q):
    """ A worker function to be launched in a separate process. Takes jobs from
        job_q - each job a list of numbers to factorize. When the job is done,
        the result (dict mapping number -> list of factors) is placed into
        result_q. Runs until job_q is empty.
    """
    while True:
        try:
            #job = job_q.get_nowait()
            #outdict = {n: factorize_naive(n) for n in job}
            crctask = job_q.get_nowait()
            outdict = tasks.calcChecksum(crctask)
            
            result_q.put(outdict)
        except Queue.Empty:
            return

def mp_factorizer(shared_job_q, shared_result_q, nprocs):
    """ 
    Create worker processes with target function,
    wait until all are finished
    """
    procs = []
    for i in range(nprocs):
        p = multiprocessing.Process(
                target=factorizer_worker,
                args=(shared_job_q, shared_result_q))
        procs.append(p)
        p.start()

    for p in procs:
        p.join()

def runclient():
    manager = make_client_manager(IP, PORTNUM, AUTHKEY)
    job_q = manager.get_job_q()
    result_q = manager.get_result_q()
    import code
    code.interact(local=locals())
    print "I see the job q as %d elements" % job_q.qsize()
    mp_factorizer(job_q, result_q, 4)

def make_client_manager(ip, port, authkey):
    """ Create a manager for a client. This manager connects to a server on the
        given address and exposes the get_job_q and get_result_q methods for
        accessing the shared queues from the server.
        Return a manager object.
    """
    class ServerQueueManager(SyncManager):
        pass

    ServerQueueManager.register('get_job_q')
    ServerQueueManager.register('get_result_q')

    manager = ServerQueueManager(address=(ip, port), authkey=authkey)
    manager.connect()

    print 'Client connected to %s:%s' % (ip, port)
    return manager

if __name__ == "__main__":
    runclient()
