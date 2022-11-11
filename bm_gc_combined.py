from pprint import pprint
from itertools import count, cycle
import gc
import pyperf

SIG_DICT = 0xd1c7 # Create new dictionary
SIG_LIST = 0x7157 # Create new list


def benchmark(depth=1000) -> float:
    t0 = pyperf.perf_counter()
    # Build tree
    root = {}
    current = root
    level = 0

    # Cycle through this list of values for each item in the tree
    POSSIBLE_VALUES = [0., 0, SIG_LIST, SIG_DICT, None, ()]
    values = cycle(POSSIBLE_VALUES)
    # Keep a master unique key for each item in the tree
    index = count()

    while level < depth:
        for _ in range(len(POSSIBLE_VALUES)):
            new_value = next(values)
            new_key = next(index)
            if new_value is SIG_LIST:
                current[new_key] = []
            elif new_value == SIG_DICT:
                new_value = dict()
                current[new_key] = new_value
                current = new_value
                break

            else:
                current[new_key] = new_value
        level += 1

    # pprint(root, depth=5)
    
    # Traverse tree and add every item to a list with a tuple (k,v)
    all_items = []
    current = root
    level = 0
    while level < depth:
        for key, value in current.items():
            if isinstance(value, dict):
                current = value
            all_items.append((key, value))
        level += 1


    # Traverse and add the all_items to every list in the tree
    current = root
    level = 0
    while level < depth:
        for key, value in current.items():
            if isinstance(value, dict):
                current = value
                break
            elif isinstance(value, list):
                value.append(all_items)
        level += 1

    # pprint(root, depth=5)

    # Now pop the parent from every list in the tree
    current = root
    level = 0
    while level < depth:
        for key, value in current.items():
            if isinstance(value, dict):
                current = value
                break
            elif isinstance(value, list):
                value.pop()
        level += 1
    # pprint(root, depth=5)

    # Now go through and remove every key containing a dictionary
    # to break the dictionary cycles
    current = root
    level = 0
    while level < depth:
        for key, value in current.items():
            if isinstance(value, dict):
                del current[key]
                current = value
                break
        level += 1
    # pprint(root, depth=5)

    # Clear the all items list
    all_items.clear()

    # Now delete the root
    del root

    return pyperf.perf_counter() - t0

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = "Benchmark for garbage collection"
    gc.collect()
    runner.bench_time_func('bm_gc_combined_defaults', benchmark)

    gc.set_threshold(50, 10, 10)
    gc.collect()

    runner.bench_time_func('bm_gc_combined_50_g0', benchmark)

    gc.set_threshold(700, 10, 10)
    gc.collect()
    runner.bench_time_func('bm_gc_combined_700_g0', benchmark)

    gc.set_threshold(5000, 10, 10)
    gc.collect()
    runner.bench_time_func('bm_gc_combined_5000_g0', benchmark)

    gc.collect()
    gc.disable()
    runner.bench_time_func('bm_gc_combined_disabled', benchmark)
