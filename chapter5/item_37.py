import select
from threading import Thread
from time import time


def slow_system_call():
    select.select([], [], [], 0.1)


def main():
    start = time()
    threads = []
    for _ in range(5):
        thread = Thread(target=slow_system_call)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end = time()
    print('Took %.3f seconds' % (end - start))

main()
