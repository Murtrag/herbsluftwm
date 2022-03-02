def time_dec(f):
    from time import perf_counter_ns
    
    def wrapper(*arg, **args):
        print(f'------------ Start timing function: {f.__name__} ------------')
        a = perf_counter_ns() 
        f(*arg, **args)
        b = perf_counter_ns() 
        per_sum = b - a
        per_sum_s = per_sum * (0.000000001)
        print(" function takes:")
        print(f"time in ns:\n{per_sum}")
        print(f"time in s:\n{per_sum_s}")
    return wrapper
