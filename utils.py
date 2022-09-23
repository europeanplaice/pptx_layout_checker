import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Optional, Union
import glob

namespaces = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def extract_pptx(path: Path, dir: Optional[Union[str, Path]] = None) -> None:
    if dir is None:
        dir = path.with_suffix("")
    with zipfile.ZipFile(path) as zf:
        zf.extractall(dir)


def parse_xml(path: Path) -> list[Optional[str]]:
    tree = ET.parse(path)
    psps = tree.getroot()[0][0].findall(
        "p:sp", namespaces)
    fonts = []


def check_func(fontlist: list[tuple[str, str]], font_to_be: str) -> Optional[dict[str, str]]:
    error_dict = {}
    for i, v in fontlist:
        if i is None:
            continue
        if i != font_to_be:
            error_dict[v] = f"Should be {font_to_be}, but {i}."
    if len(error_dict) == 0:
        return "Great, all grean."
    return error_dict


def func_to_whole_process(pathname: str, dirname: Optional[str]=None):
    extract_pptx(Path(pathname), Path(dirname))
    fontlist = []
    for i in glob.glob(str(Path(dirname).joinpath("ppt/slides/*.xml"))):
        tree = ET.parse(i)
        psps = tree.getroot()[0][0].findall(
            "p:sp", namespaces)
        for psp in psps:
            fontlist.append(function_for_all_font(psp))
    return fontlist


def function_for_all_font(psp):
    name = psp.find("p:nvSpPr", namespaces)
    if name is None:
        raise ValueError("p:nvSpPr not found")
    name = name.find("p:cNvPr", namespaces)
    if name is None:
        raise ValueError("p:nvSpPr not found")
    name = name.attrib["name"]
    font = psp.find("p:txBody", namespaces)
    if font is None:
        raise ValueError("p:txBody not found")
    font = font.find("a:p", namespaces)
    if font is None:
        raise ValueError("a:p not found")
    font_r = font.find("a:r", namespaces)
    if font_r is None:
        return None, name
    font_r = font_r.find("a:rPr", namespaces)
    if font_r is None:
        raise ValueError("a:rPr not found")
    font_endpararpr = font.find("a:endParaRPr", namespaces)
    if font_endpararpr is None:
        raise ValueError("a:endParaRPr not found")
    font_r = font_r.find("a:latin", namespaces)
    font_endpararpr = font_endpararpr.find("a:latin", namespaces)
    if font_r is None and font_endpararpr is None:
        return "default", name

    assert font_r.attrib["typeface"] == font_endpararpr.attrib["typeface"]
    return font_r.attrib["typeface"], name


if __name__ == "__main__":
    extract_pptx(Path("color_sample/shape_color_blue.pptx"))
