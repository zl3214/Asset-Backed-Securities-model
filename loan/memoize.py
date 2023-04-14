'''
Create a memoize decorator function
'''

from functools import wraps

# memoize decorator function
def Memoize(f):
    cache = f.cache = {} # use cache to store parameter sets

    @wraps(f)
    def wrapped(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache: # if parameter set not used, call function and store the result
            cache[key] = f(*args, **kwargs)
        return cache[key] # return the result corresponding to the parameter set

    return wrapped
