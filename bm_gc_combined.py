from pprint import pprint
from itertools import count, cycle
import gc
import pyperf

SIG_DICT = 0xd1c7

def benchmark(depth=100, max_width=10) -> float:
    t0 = pyperf.perf_counter()
    # Build tree
    root = {}
    current = root
    level = 0
    values = cycle([0., 0, [], SIG_DICT, None, ()])
    index = count()
    while level < depth:
        for _ in range(max_width):
            new_value = next(values)
            new_key = next(index)

            if new_value == SIG_DICT:
                new_value = dict()
                current[new_key] = new_value
                current = new_value
                break

            else:
                current[new_key] = new_value
        level += 1

    # pprint(root)
    
    # Traverse and add the parent to every list in the tree
    current = root
    level = 0
    while level < depth:
        for key, value in current.items():
            if isinstance(value, dict):
                current = value
                break
            elif isinstance(value, list):
                value.append(current)
        level += 1

    # pprint(root)
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
    # pprint(root)

    # Now go through and remove every key containing a dictionary
    # to break the dictionary cycles
    current = root
    level = 0
    while level < depth:
        for key, value in current.items():
            if isinstance(value, dict):
                current = value
            else:
                del current[key]
                break
        level += 1
    # pprint(all_dicts)
    return pyperf.perf_counter() - t0

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = "Benchmark for garbage collection"
    gc.collect()
    gc.set_threshold(50, 10, 10)
    runner.bench_time_func('bm_gc_combined_50_g0', benchmark)
    gc.set_threshold(700, 10, 10)
    runner.bench_time_func('bm_gc_combined_700_g0', benchmark)
    gc.set_threshold(5000, 10, 10)
    runner.bench_time_func('bm_gc_combined_5000_g0', benchmark)
    gc.disable()
    runner.bench_time_func('bm_gc_combined_disabled', benchmark)


