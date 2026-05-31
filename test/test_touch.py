import pytest
from pathlib import Path

# -- Local Imports ----
import sys
import os
sys.path.insert(1, os.path.dirname(__file__) + "/../src")
from utils import touch
# -- Local Imports ----

def test_touch_creates_new_file(tmp_path):
    fpath = tmp_path / "test.txt"

    existed = touch(str(fpath))

    assert existed is False
    assert fpath.exists()


def test_touch_writes_content(tmp_path):
    fpath = tmp_path / "test.txt"

    touch(str(fpath), cont="hello world")

    assert fpath.read_text() == "hello world\n"


def test_touch_existing_file_returns_true(tmp_path):
    fpath = tmp_path / "test.txt"
    fpath.write_text("original\n")

    existed = touch(str(fpath))

    assert existed is True
    assert fpath.read_text() == "original\n"


def test_touch_does_not_overwrite_existing_file(tmp_path):
    fpath = tmp_path / "test.txt"
    fpath.write_text("keep me\n")

    touch(str(fpath), cont="new contents")

    assert fpath.read_text() == "keep me\n"


def test_touch_strict_raises_if_file_exists(tmp_path):
    fpath = tmp_path / "test.txt"
    fpath.write_text("data\n")

    with pytest.raises(Exception):
        touch(str(fpath), strict=True)


def test_touch_strict_does_not_raise_for_new_file(tmp_path):
    fpath = tmp_path / "novel.txt"
    touch(str(fpath), strict=True)
    assert fpath.exists()
