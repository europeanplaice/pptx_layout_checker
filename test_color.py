from utils import extract_pptx, namespaces
import tempfile
from pathlib import Path
import pytest
import xml.etree.ElementTree as ET
import os, shutil
import tempfile
from typing import Optional
import glob

def get_name(psp):
    name = psp.find("p:nvSpPr", namespaces)
    if name is None:
        raise ValueError("p:nvSpPr not found")
    name = name.find("p:cNvPr", namespaces)
    if name is None:
        raise ValueError("p:nvSpPr not found")
    name = name.attrib["name"]
    return name


def get_text_color(psp):
    color = psp.find("p:txBody", namespaces)
    if color is None:
        raise ValueError("p:txBody not found")
    color = color.find("a:p", namespaces)
    if color is None:
        raise ValueError("a:p not found")
    color_r = color.find("a:r", namespaces)
    if color_r is None:
        raise ValueError("a:r not found")
    color_r = color_r.find("a:rPr", namespaces)
    if color_r is None:
        raise ValueError("a:rPr not found")
    solidFill = color_r.find("a:solidFill", namespaces)
    if solidFill is None:
        solidFill__srgbClr = "default"
    else:
        solidFill__srgbClr = solidFill.find("a:srgbClr", namespaces)
        if solidFill__srgbClr is not None:
            solidFill__srgbClr = solidFill__srgbClr.attrib["val"]
    highlight = color_r.find("a:highlight", namespaces)
    if highlight is None:
        highlight__srgbClr = "default"
    else:
        highlight__srgbClr = highlight.find("a:srgbClr", namespaces)
        if highlight__srgbClr is not None:
            highlight__srgbClr = highlight__srgbClr.attrib["val"]
    return solidFill__srgbClr, highlight__srgbClr


def test_extract_default():
    with tempfile.TemporaryDirectory() as dir:
        extract_pptx(Path("color_sample/default_color.pptx"), Path(dir))
        for i in glob.glob(str(Path(dir).joinpath("ppt/slides/*.xml"))):
            tree = ET.parse(i)
            psps = tree.getroot()[0][0].findall(
                "p:sp", namespaces)
            assert len(psps) > 0
            for psp in psps:
                assert get_name(psp) == "テキスト ボックス 3"
                solidFill__srgbClr, highlight__srgbClr = get_text_color(psp)
                assert solidFill__srgbClr == "default"
                assert highlight__srgbClr == "default"


def test_extract_color():
    with tempfile.TemporaryDirectory() as dir:
        extract_pptx(Path("color_sample/text_color_red.pptx"), Path(dir))
        for i in glob.glob(str(Path(dir).joinpath("ppt/slides/*.xml"))):
            tree = ET.parse(i)
            psps = tree.getroot()[0][0].findall(
                "p:sp", namespaces)
            assert len(psps) > 0
            for psp in psps:
                assert get_name(psp) == "テキスト ボックス 3"

                solidFill__srgbClr, highlight__srgbClr = get_text_color(psp)
                assert solidFill__srgbClr == "FF0000"
                assert highlight__srgbClr == "default"


def test_extract_color_highlight():
    with tempfile.TemporaryDirectory() as dir:
        extract_pptx(Path("color_sample/text_color_red_highlight.pptx"), Path(dir))
        for i in glob.glob(str(Path(dir).joinpath("ppt/slides/*.xml"))):
            tree = ET.parse(i)
            psps = tree.getroot()[0][0].findall(
                "p:sp", namespaces)
            assert len(psps) > 0
            for psp in psps:
                assert get_name(psp) == "テキスト ボックス 3"

                solidFill__srgbClr, highlight__srgbClr = get_text_color(psp)
                assert solidFill__srgbClr == "FF0000"
                assert highlight__srgbClr == "FFFF00"
