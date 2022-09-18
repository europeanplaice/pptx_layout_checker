import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Optional, Union
import tempfile

namespaces = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def extract_pptx(path: Path, dir: Union[str, Path] = None):
    if dir is None:
        dir = path.with_suffix("")
    with zipfile.ZipFile(path) as zf:
        zf.extractall(dir)


def parse_xml(path: Path) -> list[Optional[str]]:
    tree = ET.parse(path)
    psps = tree.getroot()[0][0].findall(
        "p:sp", namespaces)
    fonts = []
    for psp in psps:
        font = psp.find("p:txBody", namespaces) \
                  .find("a:p", namespaces) \
                  .find("a:r", namespaces) \
                  .find("a:rPr", namespaces) \
                  .find("a:latin", namespaces)
        if font is None:
            fonts.append(None)
        else:
            fonts.append(font.attrib["typeface"])
    return fonts


if __name__ == "__main__":
    extract_pptx(Path("different_font.pptx"))
    parse_xml(Path("different_font.pptx").with_suffix(
        "").joinpath("ppt/slides/slide1.xml"))
