import pytest

# -- Local Imports ----
import sys
import os
sys.path.insert(1, os.path.dirname(__file__) + "/../src")
print(sys.path)
import utils as mypy
# -- Local Imports ----

def inc(i):
    j = i + 1
    return j

def thd_uni_common_case():
    inp = [1, 2, 3, 4]
    res = mypy.thread_uni(
        inp,
        (lambda i : map(inc, i)),
        list,
        sum
    )
    assert(inp == [1,2,3,4])
    assert(res == 14)

def thread_empty():
    try:
        mypy.thread_uni()
        pytest.fail("thread called without args should cause an exception")
    except Exception as e:
        assert("thread called without args" in e.args[0])

def thread_bad_order():
    try:
        mypy.thread_uni(inc, [1,2,3])
        pytest.fail("thread called out of order should cause an exception")
    except TypeError as e:
        assert("'list' object is not callable" in e.args[0])

    try:
        mypy.thread_f(inc, [inc])
        pytest.fail("thread called out of order should cause an exception")
    except TypeError as e:
        assert("unsupported operand type(s)" in e.args[0])


def thd_last_common_case():
    res = mypy.thread_l(
        [1, 2, 3, 4],
        (map, inc),
        mypy.lst,
        sum
    )
    assert(res == 14)

def thread_bad_fn_vec():
    try:
        mypy.thread_f(
            {'a' : 2},
            [1, inc]
        )
        pytest.fail("function vector mallformed")
    except TypeError as e:
        assert("function vector must start with an fn. Recieved: <class int>" in e.args[0])

def thd_first_common_case():
    init = {'a' : 5, 'b' : 10}
    res = mypy.thread_f(
        init,
        (mypy.merge, {'a' : 15}),
        (mypy.merge, {'c' : 20})
    )
    assert(init == {'a' : 5, 'b' : 10})
    assert(res  == {'a' : 15, 'b' : 10, 'c' : 20})

def test_thread():
    thd_uni_common_case()
    thd_last_common_case()
    thd_first_common_case()

    thread_empty()
    thread_bad_order()
