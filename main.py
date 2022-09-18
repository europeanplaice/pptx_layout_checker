from utils import extract_pptx, extract_fonts
from pathlib import Path
import tempfile
import argparse
import glob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()

    path = Path(args.path)
    fonts = []
    with tempfile.TemporaryDirectory() as dir:
        extract_pptx(path, dir)
        for slide in glob.glob(str(Path(dir).with_suffix(
                "").joinpath("ppt/slides/*.xml"))):
            fonts += extract_fonts(slide)
    if len(set(fonts)) > 1:
        print("This pptx contains different fonts.")
        print(fonts)
    else:
        print("Great, this pptx contains the same font.")


if __name__ == "__main__":
    main()
