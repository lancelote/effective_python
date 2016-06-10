from collections import namedtuple
import os
from tempfile import TemporaryDirectory
from threading import Thread

File = namedtuple('File', 'name text')


class InputData(object):

    def read(self):
        raise NotImplementedError


class PathInputData(object):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as file:
            return file.read()


class Worker(object):

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


class LineCountWorker(Worker):

    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def write_test_files(tmpdir):
    files = [
        File('file1', '1\n2\n3'),
        File('file2', '1\n2\n3\n4')
    ]

    for file in files:
        with open(os.path.join(tmpdir, file.name), 'w') as f:
            f.write(file.text)


def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


def execute(workers):
    threads = [Thread(target=worker.map) for worker in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


def map_reduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


def main():
    with TemporaryDirectory() as tmpdir:
        write_test_files(tmpdir)
        result = map_reduce(tmpdir)

    print('There are', result, 'lines')

if __name__ == '__main__':
    main()
