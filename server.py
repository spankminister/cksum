import argparse
import multiprocessing
from multiprocessing.managers import SyncManager
import time
import Queue

from PyCRC.CRCCCITT import CRCCCITT

BEGIN_OFFSET = 0
END_OFFSET = 1
FILE = "/Users/spanky/Dropbox/ctf/gamecube/memorycards/bak.raw"

PORTNUM=1337
AUTHKEY = "asdf"

def make_nums(N):
    """ Create N large numbers to factorize.
    """
    nums = [999999999999]
    for i in xrange(N):
        nums.append(nums[-1] + 2)
    return nums

def make_server_manager(port, authkey):
    """ Create a manager for the server, listening on the given port.
        Return a manager object with get_job_q and get_result_q methods.
    """
    job_q = Queue.Queue()
    result_q = Queue.Queue()

    # This is based on the examples in the official docs of multiprocessing.
    # get_{job|result}_q return synchronized proxies for the actual Queue
    # objects.
    class JobQueueManager(SyncManager):
        pass

    JobQueueManager.register('get_job_q', callable=lambda: job_q)
    JobQueueManager.register('get_result_q', callable=lambda: result_q)

    manager = JobQueueManager(address=('', port), authkey=authkey)
    manager.start()
    print 'Server started at port %s' % port
    return manager

def runserver():
    # Start a shared manager server and access its queues
    manager = make_server_manager(PORTNUM, AUTHKEY)
    shared_job_q = manager.get_job_q()
    shared_result_q = manager.get_result_q()

    # Add tasks
    #add_tasks()
    N = 999
    nums = make_nums(N)

    # The numbers are split into chunks. Each chunk is pushed into the job
    # queue.
    chunksize = 43
    for i in range(0, len(nums), chunksize):
        shared_job_q.put(nums[i:i + chunksize])

    # Wait until all results are ready in shared_result_q
    numresults = 0
    resultdict = {}
    try:
        while numresults < N:
            outdict = shared_result_q.get()
            resultdict.update(outdict)
            numresults += len(outdict)
    except KeyboardException:
        print("Caught CTRL+C, Exiting...")

    finally:
        # Sleep a bit before shutting down the server - to give clients time to
        # realize the job queue is empty and exit in an orderly way.
        time.sleep(2)
        manager.shutdown()

def parseargs():
    parser = argparse.ArgumentParser(description='Find CRC16 checksum in GC save file.')

    parser.add_argument('-b', '--begin', help='starting offset')
    parser.add_argument('-e', '--end', help='ending offset')
    parser.add_argument('-f', '--file', help='filename')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parseargs()
    runserver()

