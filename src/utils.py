from pprint import pformat
from functools import reduce
import sys

# ---- System Utils ------------------------------------------------------
def throw_err(msg):
    '''Throws a general exception without a traceback.'''
    sys.tracebacklimit = 0
    raise Exception(msg)
# ---- System Utils ------------------------------------------------------


# ---- Functional Utils ---------------------------------------------------
def spec_map(required_keys, mp):
    '''Loops through required keys, making sure map has them,
       thorws an en exception if one is missing'''
    check_key = (lambda k :
        None
        if k in mp.keys() else
        throw_err("Missing required key: '"+ k +"' in map:\n" \
                  + pformat(mp, compact=True))
    )
    list(map(check_key, required_keys))

def l_contains(l, el):
    '''Does list l contain element el? Returns a boolean'''
    return (l.count(el) > 0)

def merge(dict1, dict2, *dicts):
    '''Merge dictionaries 1 through n into a single dictionary.
       Non-mutating, returns a new dictionary withougt modifing inputs.'''
    dictionaries = [dict1] + [dict2] + list(dicts)
    return reduce((lambda d1, d2 : {**d1, **d2}), dictionaries)

# Thread Functions
def _thd_first(h,t=None):
    return t[0](h, *t[1:])

def _thd_last(h,t=None):
    return t[0](*t[1:], h)

def _thd_uni(h,t=None):
    return (t(h) if t else h)

def _thd_wrap(thd_fn):
    def fn(h,t=None):
        if(callable(t)): return _thd_uni(h,t)
        if(isinstance(t, list) or isinstance(t,tuple)):
            if(not callable(t[0])):
                sys.tracebacklimit = 0
                raise TypeError(
                    "function vector must start with an fn. Recieved:"\
                    + str(type(t)) + " - list - " + str(t)
                )
            return thd_fn(h,t)
        if(t is None):   return h
        else:
            sys.tracebacklimit = 0
            raise TypeError(
                "thread element must be a function or list. Recieved:" \
                + str(type(t)) + " - " + str(t))
    return fn

def lst(lazy_seq):
    '''Support function for threads: When passing list() as a parameter, python
    sometimes passes the list type instead. This function ensures you get the
    list function'''
    return list(lazy_seq)

def thread(*fns, thd_fn=_thd_uni):
    sys.tracebacklimit = 0
    if (not fns): raise Exception("thread called without args")
    return reduce(thd_fn, fns)

def thread_l(*fns):
    '''Instead of nesting functions, achieve function composition with a list.
    The output of the previous list element is used as the *last* argument for the current line.
    Elements in this list can be:
    * A primiative datastructure (lists, vectors, maps, scalers, etc...)
    * A unitary function (in which the output from the previous line is simply used as the input for the function)
    * A 'function vector' which has the following terms:
      [<function>, arg1, arg2, ... argn]
      The output from the previous line will be added as argn+1
    Example:

    res = thread_l(
        [1, 2, 3, 4],
        (map, (lambda x : x+1)),
        lst,
        sum
    )
    assert(res == 14)
    '''
    return thread(*fns, thd_fn=_thd_wrap(_thd_last))

def thread_f(*fns):
    '''Instead of nesting functions, achieve function composition with a list.
    The output of the previous element will be the *first* input to the function of the current element.
    Elements in this list can be:
    * A primiative (list, vector, dictionaries, scalers, etc...)
    * A unitary function (in which the output from the previous line is used as the argument for this function)
    * A 'function vector' which has the following terms:
      [<function>, arg1, arg2, ... argn]
      The output from the previous line will be added as argn+1
    Expample:

    res = thread_f(
        {'a' : 5, 'b' : 10},
        (merge, {'a' : 15}),
        (merge, {'c' : 20})
    )
    assert(res == {'a' : 15, 'b' : 10, 'c' : 20})

    '''
    return thread(*fns, thd_fn=_thd_wrap(_thd_first))

def thread_uni(*fns):
    '''Default thread function:
    Instead of nesting functions, achieve function composition with a list.

    Takes UNITARY functions only.

    This function takes output/data from the first statement,
    then calls the next function in the list with that output.

    Example:

    res = thread_uni(
        [1, 2, 3, 4],
        (lambda i : map((lambda x : x+1), i)),
        list,
        sum
    )
    assert(res=14)

    '''
    return thread(*fns)
# ---- Functional Utils ---------------------------------------------------
