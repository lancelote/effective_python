from threading import Lock, Thread


class LockingCounter(object):

    def __init__(self):
        self.count = 0
        self.lock = Lock()

    def increment(self, offset):
        with self.lock:
            self.count += offset


def worker(how_many, counter):
    for _ in range(how_many):
        # Read data from the sensor
        # ...
        counter.increment(1)


def run_threads(func, how_many, counter):
    threads = []
    for _ in range(5):
        args = (how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def main():
    how_many = 10**5
    counter = LockingCounter()
    run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % (5*how_many, counter.count))

main()
