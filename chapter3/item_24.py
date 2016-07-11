from collections import namedtuple
import os
from tempfile import TemporaryDirectory
from threading import Thread

File = namedtuple('File', 'name text')


class GenericInputData(object):

    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputData):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker(object):

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker):

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


def map_reduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


def main():
    with TemporaryDirectory() as tmpdir:
        write_test_files(tmpdir)
        config = {'data_dir': tmpdir}
        result = map_reduce(LineCountWorker, PathInputData, config)

    print('There are', result, 'lines')

if __name__ == '__main__':
    main()
