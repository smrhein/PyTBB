from multiprocessing import Process, Lock 
from Queue import Empty 
import time 
import traceback
import sys
# from  pytbb.pipeline import Queue
import multiprocessing as mp
# from multiprocessing import Queue
import Queue

start = time.time() 

def now(): 
    return time.time() - start 

class test_lock_process(object): 
    def __init__(self, lock, id, queue): 
        self.lock = lock 
        self.id = id 
        self.queue = queue 
        self.read_lock() 

    def read_lock(self): 
        for _ in xrange(2 ** 4):

            self.lock.acquire()
            
            self.queue.put((True, now(), self.id))
            # print '%s got lock' % self.id
            
#             time.sleep(1e-2)  # .2) 
            
            self.queue.put((False, now(), self.id)) 

            self.lock.release()
            # print '%s   rel lock' % self.id

def test_lock(processes=10, lock=Lock(), queue=None): 

    print_result = False 
    if queue == None: 
        print_result = True 
        queue = Queue()

    procs = [] 
    for i in xrange(processes): 
        procs.append(Process(target=test_lock_process, args=(lock, i, queue,))) 

    start = time.time()
    for t in procs: 
        t.start() 
    for t in procs: 
        t.join() 
    end = time.time()
    
    print end - start
    res = [(None, 0, None)]
    i = 0
    if print_result: 
        try: 
            while True:
                res.append(queue.get(block=False))
                if res[-1][0] == res[-2][0]:                    
                    sys.stderr.write("{}:\n".format(i))
                    for r in res[-2 ** 2:]:
                        sys.stderr.write("{}\n".format(r))
                    sys.stderr.write("\n")
                i += 1
        except Empty: 
            sys.stderr.write("{}:".format(i))

_manager = mp.Manager()
_manager.register("Queue", Queue.Queue)
Queue = _manager.Queue

if __name__ == "__main__": 
    test_lock(processes=2 ** 6)
