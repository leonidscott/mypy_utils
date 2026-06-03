from pathlib import Path
import pytest

# -- Local Imports ----
import sys
import os
sys.path.insert(1, os.path.dirname(__file__) + "/../src")
from utils import rm
# -- Local Imports ----

def test_rm_existing(tmp_path):
    """Existing file should be removed and return True."""
    f = tmp_path / "test.txt"
    f.write_text("hello")

    assert f.exists()

    removed = rm(str(f))

    assert removed is True
    assert not f.exists()


def test_rm_missing(tmp_path):
    """Missing file should return False and not raise."""
    f = tmp_path / "does_not_exist.txt"

    assert not f.exists()

    removed = rm(str(f))

    assert removed is False
    assert not f.exists()


def test_rm_idempotent(tmp_path):
    """Calling rm twice should not raise."""
    f = tmp_path / "test.txt"
    f.write_text("hello")

    assert rm(str(f)) is True
    assert rm(str(f)) is False


def test_rm_empty_file(tmp_path):
    """Empty files should be removable."""
    f = tmp_path / "empty.txt"
    f.touch()

    assert f.exists()

    removed = rm(str(f))

    assert removed is True
    assert not f.exists()
