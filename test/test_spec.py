import pytest

# -- Local Imports ----
import sys
import os
sys.path.insert(1, os.path.dirname(__file__) + "/../src")
print(sys.path)
import utils as mypy
# -- Local Imports ----

def working_case():
    required_keys = ['run_root', 'name', 'tec_temp', 'run_dir']
    map_in = {'grid': '/project/users/va-group/qualitative-tests-large-files/cylinder-grid.h5', 'conn': '/project/users/va-group/qualitative-tests-large-files/cylinder-conn.h5', 'run_root': '/project/users/va-group/qualitative-tests/cylinder', 'gas_file': '/project/users/va-group/qualitative-tests/cylinder/air-11sp-park93-dplr.dat', 'input_file': '/project/users/va-group/qualitative-tests/cylinder/input-template.txt', 'slurm_temp': '/project/users/va-group/qualitative-tests/cylinder/slurm-template.txt', 'exports': ['export HDF5_USE_FILE_LOCKING=FALSE'], 'post_file': '/project/users/va-group/qualitative-tests/cylinder/post.scr', 'tec_temp': '/project/users/va-group/qualitative-tests/cylinder/plot-stag.mcr', 'name': 'cylinder-10kms-ivib2-us3d-1.1.8', 'modules': ['us3d-license', 'us3d-debug/1.1.8-p3/openmpi/4.1.0/gnu/11.3.0'], 'ivib': 2, 'run_dir' : 'I am a run dir'}

    try:
        mypy.spec_map(required_keys,map_in)
        assert 2 == 2, "Spec map did not throw an error"
    except:
        pytest.fail("Threw error when it wasn't supposed to")

def failing_case():
    required_keys = ['run_root', 'name', 'tec_temp', 'run_dir']
    map_in = {'grid': '/project/users/va-group/qualitative-tests-large-files/cylinder-grid.h5', 'conn': '/project/users/va-group/qualitative-tests-large-files/cylinder-conn.h5', 'run_root': '/project/users/va-group/qualitative-tests/cylinder', 'gas_file': '/project/users/va-group/qualitative-tests/cylinder/air-11sp-park93-dplr.dat', 'input_file': '/project/users/va-group/qualitative-tests/cylinder/input-template.txt', 'slurm_temp': '/project/users/va-group/qualitative-tests/cylinder/slurm-template.txt', 'exports': ['export HDF5_USE_FILE_LOCKING=FALSE'], 'post_file': '/project/users/va-group/qualitative-tests/cylinder/post.scr', 'tec_temp': '/project/users/va-group/qualitative-tests/cylinder/plot-stag.mcr', 'name': 'cylinder-10kms-ivib2-us3d-1.1.8', 'modules': ['us3d-license', 'us3d-debug/1.1.8-p3/openmpi/4.1.0/gnu/11.3.0'], 'ivib': 2}

    try:
        mypy.spec_map(required_keys, map_in)
        # If we get here, an exception did not happen. Throw eror
        pytest.fail("Did not throw an error when it should have")
    except Exception as e:
        assert ("Missing required key" in e.args[0])

def corner_cases():
    # Empty Required Keys
    lack_of_req_keys = []
    full_map = {'a' : 1, 'b' : 2}
    try:
        mypy.spec_map(lack_of_req_keys, full_map)
        assert 2 == 2, "Did not throw an error"
    except:
        pytest.fail("Threw error when it wasn't supposed to")


    # Empty Map
    full_keys = ['r1', 'r2']
    empty_map = {}
    try:
        mypy.spec_map(full_keys, empty_map)
        # If we get here, an exception did not happen. Throw eror
        pytest.fail("Did not throw an error when it should have")
    except Exception as e:
        assert ("Missing required key" in e.args[0])

    # Both Empty
    try:
        mypy.spec_map(lack_of_req_keys, empty_map)
        assert 2 == 2, "Did not throw an error"
    except:
        pytest.fail("Threw error when it wasn't supposed to")


def test_spec_map():
    working_case()
    failing_case()
    corner_cases()
