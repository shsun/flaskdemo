import cProfile as profiler
import gc, pstats, time
import os, sys


def profile(fn):
    def wrapper(*args, **kw):
        elapsed, stat_loader, result = _profile("foo.txt", fn, *args, **kw)
        stats = stat_loader()
        stats.sort_stats('cumulative')
        stats.print_stats()
        # uncomment this to see who's calling what
        stats.print_callers()
        print '-------->>', elapsed, stat_loader, result
        return result

    return wrapper


def _profile(filename, fn, *args, **kw):
    load_stats = lambda: pstats.Stats(filename)
    gc.collect()

    began = time.time()
    profiler.runctx('result = fn(*args, **kw)', globals(), locals(),
                    filename=filename)
    ended = time.time()

    return ended - began, load_stats, locals()['result']
