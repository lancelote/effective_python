import gc
import tracemalloc

found_objects = gc.get_objects()
print('{} objects before'.format(len(found_objects)))


class Something(object):
    def __init__(self, pk):
        self.pk = pk


x = [Something(i) for i in range(100)]

found_objects = gc.get_objects()
print('{} objects after'.format(len(found_objects)))

# Tracemalloc
tracemalloc.start(10)

time1 = tracemalloc.take_snapshot()
y = [Something(i) for i in range(100)]
time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'lineno')
for stat in stats[:3]:
    print(stat)

stats = time2.compare_to(time1, 'traceback')
top = stats[0]
print('\n'.join(top.traceback.format()))
