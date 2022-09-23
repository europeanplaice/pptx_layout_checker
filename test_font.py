from utils import extract_pptx, namespaces, check_func, func_to_whole_process, function_for_all_font
import tempfile
from pathlib import Path
import pytest
import xml.etree.ElementTree as ET
import os, shutil
import tempfile
from typing import Optional


@pytest.fixture
def prepare_folder():
    with tempfile.TemporaryDirectory() as dir:
        yield Path(dir)


def test_default_font():
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process("font_sample/default_font.pptx", dir)
        assert set(fontlist) == set([("default", "テキスト ボックス 3")])
    assert check_func(fontlist, "default") == "Great, all grean."


def test_font_abadi():
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process("font_sample/font_abadi.pptx", dir)
        assert set(fontlist) == set([("Abadi", "テキスト ボックス 3")])
    assert check_func(fontlist, "Abadi") == "Great, all grean."


def test_font_shape_without_text():
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process("font_sample/shape_without_text.pptx", dir)
        assert set(fontlist) == set([(None, "正方形/長方形 3")])


def test_font_shape_default_font():
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process("font_sample/shape_with_default_font.pptx", dir)
        assert set(fontlist) == set([("default", "正方形/長方形 3")])
    assert check_func(fontlist, "default") == "Great, all grean."


def test_font_shape_font_abadi():
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process("font_sample/shape_with_font_abadi.pptx", dir)
    result = check_func(fontlist, "Abadi")
    assert result == "Great, all grean."


def test_font_abadi_and_default():
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process("font_sample/font_abadi_and_default.pptx", dir)
    result = check_func(fontlist, "Abadi")
    assert result == {"テキスト ボックス 2": "Should be Abadi, but default."}


def test_font_abadi_default_no():
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process("font_sample/font_abadi_and_default_and_shape_with_no_text.pptx", dir)
    assert set(fontlist) == set([(None, '楕円 1'),
                                 ('Abadi', 'テキスト ボックス 3'),
                                 ('default', 'テキスト ボックス 2'),
                                 (None, '四角形: 角を丸くする 4')])
    result = check_func(fontlist, "default")
    assert result == {
        "テキスト ボックス 3": "Should be default, but Abadi.",
        }
