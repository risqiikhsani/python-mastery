"""
Concurrency: Threading and multiprocessing
"""

import threading
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# Threading example
def thread_task(name: str, duration: float):
    print(f"Thread {name} starting")
    time.sleep(duration)
    print(f"Thread {name} finished")


# Create and start threads
threads = []
for i in range(3):
    t = threading.Thread(target=thread_task, args=(f"T{i}", 0.5))
    threads.append(t)
    t.start()

for t in threads:
    t.join()


# ThreadPoolExecutor (cleaner API)
def cpu_task(n: int) -> int:
    return sum(i * i for i in range(n))


with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(cpu_task, 10000) for _ in range(8)]
    results = [f.result() for f in futures]
    print(f"Thread results: {results[:3]}...")


# Multiprocessing for CPU-bound tasks
def parallel_task(n: int) -> int:
    return sum(i ** 2 for i in range(n))


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(parallel_task, 10000) for _ in range(8)]
        results = [f.result() for f in futures]
        print(f"Process results: {results[:3]}...")


# Thread-safe counter with Lock
class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1


def increment_worker(counter: SafeCounter, iterations: int):
    for _ in range(iterations):
        counter.increment()


counter = SafeCounter()
threads = [
    threading.Thread(target=increment_worker, args=(counter, 10000))
    for _ in range(4)
]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"Counter value: {counter.count} (expected: 40000)")


# Queue for thread communication
from queue import Queue


def producer(queue: Queue, items: list):
    for item in items:
        queue.put(item)
        print(f"Produced: {item}")


def consumer(queue: Queue, count: int):
    for _ in range(count):
        item = queue.get()
        print(f"Consumed: {item}")
        queue.task_done()


queue = Queue()
t1 = threading.Thread(target=producer, args=(queue, [1, 2, 3]))
t2 = threading.Thread(target=consumer, args=(queue, 3))
t1.start()
t2.start()
t1.join()
t2.join()