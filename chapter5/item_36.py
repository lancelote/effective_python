import os
import subprocess
from time import time


def run_sleep(period):
    process = subprocess.Popen(['sleep', str(period)])
    return process


def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    proc.stdin.write(data)
    proc.stdin.flush()  # Ensure the child gets the data
    return proc


def example1():
    process = subprocess.Popen(
        ['echo', 'Hello from the child!'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    print(out.decode('utf-8'))


def example2():
    """Working while child process does it's job"""
    process = subprocess.Popen(['sleep', '0.1'])
    while process.poll() is None:
        print('Working...')
    print('Exit status', process.poll())


def example3():
    """Multiple child processes"""
    start = time()
    processes = []
    for _ in range(10):
        process = run_sleep(0.1)
        processes.append(process)

    for process in processes:
        process.communicate()
    end = time()
    print('Finished in %.3f seconds' % (end - start))


def example4():
    """Pipe data in and out child processes"""

    processes = []
    for _ in range(3):
        data = os.urandom(10)
        process = run_openssl(data)
        processes.append(process)

    for process in processes:
        out, err = process.communicate()
        print(out[-10:])


def example5():
    """Connect multiple processes via pipe (openssl -> md5sum)"""
    def run_md5(input_stdin):
        process = subprocess.Popen(
            ['md5sum'],
            stdin=input_stdin,
            stdout=subprocess.PIPE
        )
        return process

    input_processes = []
    hash_processes = []
    for _ in range(3):
        data = os.urandom(10)
        input_process = run_openssl(data)
        input_processes.append(input_process)
        hash_process = run_md5(input_process.stdout)
        hash_processes.append(hash_process)

    for input_process in input_processes:
        input_process.communicate()
    for hash_process in hash_processes:
        out, err = hash_process.communicate()
        print(out.strip())


def example6():
    """Process timeout to prevent blocking and etc."""
    process = run_sleep(10)
    try:
        process.communicate(timeout=0.1)
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait()
    print('Exit status', process.poll())  # Exit status -15

example6()
