from queue import Queue
from threading import Thread


class ClosableQueue(Queue):

    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return  # Cause the thread to exit
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):

    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0  # How many times the worker checked for data
        self.work_done = 0

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


def download(arg):
    print('download')
    return arg


def resize(arg):
    print('resize')
    return arg


def upload(arg):
    print('upload')
    return arg


def main():
    download_queue = ClosableQueue()
    resize_queue = ClosableQueue()
    upload_queue = ClosableQueue()
    done_queue = ClosableQueue()
    threads = [
        StoppableWorker(download, download_queue, resize_queue),
        StoppableWorker(resize, resize_queue, upload_queue),
        StoppableWorker(upload, upload_queue, done_queue)
    ]
    for thread in threads:
        thread.start()
    for _ in range(1000):
        download_queue.put(object())
    download_queue.close()
    download_queue.join()
    resize_queue.close()
    resize_queue.join()
    upload_queue.close()
    upload_queue.join()
    print(done_queue.qsize(), 'items finished')

main()
