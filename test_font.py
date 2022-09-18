from utils import extract_pptx, parse_xml
from pathlib import Path


def test_font_on_different_font():
    extract_pptx(Path("different_font.pptx"))
    fonts = parse_xml(Path("different_font.pptx").with_suffix(
        "").joinpath("ppt/slides/slide1.xml"))
    assert len(set(fonts)) != 1


def test_font_on_same_font():
    extract_pptx(Path("same_font.pptx"))
    fonts = parse_xml(Path("same_font.pptx").with_suffix(
        "").joinpath("ppt/slides/slide1.xml"))
    assert len(set(fonts)) == 1
