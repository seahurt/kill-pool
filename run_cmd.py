import signal
from threading import Thread
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
from queue import Queue
import fire


def signal_handle(signum, frame):
    print(f'sig: {signum} received from cmd...')
    raise SystemExit('exit...')


def worker(n):
    time.sleep(5)
    print(f'worker {n} finished')


def queued_worker(n, q):
    info = q.get()
    worker(n)
    q.put(info)

def run_as_threads():
    signal.signal(signal.SIGINT, signal_handle)
    signal.signal(signal.SIGTERM, signal_handle)
    q = Queue()
    q.put(1)
    q.put(1)
    q.put(1)
    pool = []
    for x in range(10):
        t = Thread(target=queued_worker, args=(x, q), daemon=True)
        pool.append(t)
        t.start()
    for x in pool:
        x.join()



def run_as_process_pool():
    pool = ProcessPool(3)
    for x in range(10):
        pool.apply_async(worker, args=(x,))
    pool.close()
    pool.join()


def run_as_thread_pool():
    pool = ThreadPool(3)
    for x in range(10):
        pool.apply_async(worker, args=(x,))
    pool.close()
    pool.join()


def run_as_thread_exc_pool():
    with ThreadPoolExecutor(max_workers=3) as ex:
        for x in range(10):
            ex.submit(worker, x)

def run_as_process_exc_pool():
    with ProcessPoolExecutor(max_workers=3) as ex:
        for x in range(10):
            ex.submit(worker, x)


if __name__ == "__main__":
    import os
    print(os.getpid())
    fire.Fire()
