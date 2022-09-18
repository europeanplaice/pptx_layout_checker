from utils import extract_pptx, extract_fonts, get_unique_fonts
from pathlib import Path
import pytest
import json
import tempfile
import glob


@pytest.fixture
def config():
    with open("config.json", "r") as f:
        _config = json.load(f)
    return _config


def test_font_config(config):
    if config["only_one_font"] is True:
        with tempfile.TemporaryDirectory() as dir:
            extract_pptx(Path(config["filepath"]), dir)
            fonts = []
            for slide in glob.glob(str(Path(dir).with_suffix(
                    "").joinpath("ppt/slides/*.xml"))):
                fonts += extract_fonts(slide)
                fonts = extract_fonts(Path(dir).joinpath("ppt/slides/slide1.xml"))
                assert len(get_unique_fonts(fonts)) == 1

# def test_color_config(config):

