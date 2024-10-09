import pytest

# -- Local Imports ----
import sys
import os
sys.path.insert(1, os.path.dirname(__file__) + "/../src")
print(sys.path)
import utils as mypy
# -- Local Imports ----

def test_merge():
    # Default Case
    assert \
    mypy.merge(
            {'a' : 1},
            {'b' : {'1' : 1, '2' : [1, 2]}},
            {'c' : "three", 'a' : 5}
    ) \
    == {'a' : 5,
        'b' : {'1' : 1, '2' : [1, 2]} ,
        'c' : "three"}

    # Identity Case
    with pytest.raises(TypeError): mypy.merge({'a' : 'a'}) == {'a' : 'a'}

    # Zero Case
    with pytest.raises(TypeError): mypy.merge() == {}
