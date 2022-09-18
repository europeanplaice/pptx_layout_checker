import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Optional, Union

namespaces = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def get_unique_fonts(fonts) -> list[Optional[str]]:
    font_names = []
    for font in fonts:
        if font["font_name"] is None:
            continue
        font_names.append(font["font_name"])
    return list(set(font_names))


def extract_pptx(path: Path, dir: Union[str, Path] = None):
    if dir is None:
        dir = path.with_suffix("")
    with zipfile.ZipFile(path) as zf:
        zf.extractall(dir)


def extract_fonts(path: Path) -> list[dict[str, str]]:
    tree = ET.parse(path)
    psps = tree.getroot()[0][0].findall(
        "p:sp", namespaces)
    fonts: list[dict[str, str]] = []
    for psp in psps:
        background_color = psp.find("p:spPr", namespaces)
        try:
            background_color = background_color.find("p:solidFill", namespaces)
            background_color = background_color.find("p:srgbClr", namespaces)
        except AttributeError:
            background_color = None
        text_color = psp.find("p:txBody", namespaces)
        text_color = text_color.find("a:p", namespaces)
        text_color = text_color.find("a:r", namespaces)
        text_color = text_color.find("a:rPr", namespaces)
        try:
            solidFill = text_color.find("a:solidFill", namespaces) \
                                  .find("p:srgbClr", namespaces).attrib["val"]
        except AttributeError:
            solidFill = None
        try:
            highlight = text_color.find("a:highlight", namespaces) \
                                  .find("p:srgbClr", namespaces).attrib["val"]
        except AttributeError:
            highlight = None
        name = psp.find("p:nvSpPr", namespaces)
        name = name.find("p:cNvPr", namespaces).attrib["name"]
        try:
            font = psp.find("p:txBody", namespaces) \
                      .find("a:p", namespaces) \
                      .find("a:r", namespaces)
        except AttributeError:
            font = None
            fonts.append({"object_name": name, "font_name": font})
            continue
        if font is None:
            fonts.append({"object_name": name, "font_name": font})
            continue
        try:
            font = font.find("a:rPr", namespaces) \
                       .find("a:latin", namespaces)
        except AttributeError:
            font = "default"
        if font == "default":
            fonts.append({"object_name": name, "font_name": font})
        else:
            fonts.append({"object_name": name, "font_name": font.attrib["typeface"]})
    return fonts


if __name__ == "__main__":
    extract_pptx(Path("different_font.pptx"))
    extract_fonts(Path("different_font.pptx").with_suffix(
        "").joinpath("ppt/slides/slide1.xml"))
