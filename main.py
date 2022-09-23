from utils import func_to_whole_process, check_func
from pathlib import Path
import tempfile
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()

    path = Path(args.path)
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process(path, dir)
    print(check_func(fontlist, "default"))


if __name__ == "__main__":
    main()
