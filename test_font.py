from utils import extract_pptx, extract_fonts, get_unique_fonts
from pathlib import Path
import pytest
import json
import tempfile


def test_font_on_different_font(config):
    extract_pptx(Path("different_font.pptx"))
    fonts = extract_fonts(Path("different_font.pptx").with_suffix(
        "").joinpath("ppt/slides/slide1.xml"))
    assert len(get_unique_fonts(fonts)) != 1


def test_font_on_same_font():
    extract_pptx(Path("same_font.pptx"))
    fonts = extract_fonts(Path("same_font.pptx").with_suffix(
        "").joinpath("ppt/slides/slide1.xml"))
    assert len(get_unique_fonts(fonts)) == 1
