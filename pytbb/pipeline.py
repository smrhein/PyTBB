import itertools
from Queue import Empty, Full, Queue, PriorityQueue
from threading import Lock, Semaphore, Event, BoundedSemaphore, Condition, RLock
from multiprocessing.pool import ThreadPool as Pool

class _DummyQueue:
    pass

class _DummyLock:
    pass

def _runner(stage):
    try:
        stage.run()
    finally:
        stage.__exit__(None, None, None)
        
# filters:
# input
# filter
# output
# max_live_tokens
# is_serial
# is_ordered
# is_finalizing
# is_closing
# is_closed    
    
class _stage(object):
    def __init__(self, fil, serial, ordered, finalize, in_q, out_q, tokens):
        pass
    def __enter__(self):
        raise NotImplementedError
    def run(self):
        raise NotImplementedError
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError

    
class _only_stage(_stage):
    def __enter__(self):
        if self._end_in_evt.is_set():
            if not self._worker_sem.acquire(blocking=False):
                self._end_out_evt.set()
                raise RuntimeError("stage has completed execution")
            else:
                self._worker_sem.release()
        elif self._token_sem.acquire(blocking=False) and (not self._filter.is_serial or self._serial_lck.acquire()):
            self._worker_sem.release()
            return True
        return False
    def run(self):
        try:
            if self._filter(None) is None:
                self._end_in_evt.set()
        except:
            self._finalize_evt.set()
            raise
    def __exit__(self, exc_type, exc_value, traceback):        
        self._worker_sem.acquire()
        if self._filter.is_serial: self._serial_lck.release()
        self._token_sem.release()            
        self._task_sem.release()
        return False


class pipeline_filter(object):
    def __init__(self, mode="serial_in_order"):
        if mode == "serial_in_order":
            self._is_serial = True
            self._is_ordered = True
        else:
            raise NotImplementedError
    @property
    def is_serial(self):
        return self._is_serial
    @property
    def is_ordered(self):
        return self._is_ordered
    def __call__(self, item):
        raise NotImplementedError
    def finalize(self, item):
        pass

# filters:
# input
# filter
# output
# max_live_tokens
# is_serial
# is_ordered
# is_finalizing
# is_closing
# is_closed
class pipeline(object):
    def __init__(self):
        self._filters = []
    def add_filter(self, fil):
        if fil in self._filters:
            raise ValueError("The filter {} must not already be in a pipeline.".format(fil))
        self._filters.append(fil)
    def run(self, max_number_of_live_tokens=None, group=None):
        group = Pool()
        try:
            stages = []
            
            in_q = _DummyQueue()
            end_in = Event()
            if self._filters[0].is_serial:
                serial = Lock()
            else:
                serial = _DummyLock()
            if self._filters[0].is_ordered:
                out_q = PriorityQueue()
            else:
                out_q = Queue()
            
            
            for i, f in enumerate(self._filters):
                pass
                    
            send_q, recv_q = Queue(), Queue()
            
            group.close()
        except:
            group.terminate()
        finally:
            group.join()
    def clear(self):
        self._filters = []



if __name__ == '__main__':
    import random
    import os
    import sys
    import time    
