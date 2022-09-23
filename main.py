from utils import func_to_whole_process, check_func
import tempfile
import json


def main():
    with open("config.json", "r") as f:
        config = json.load(f)
    with tempfile.TemporaryDirectory() as dir:
        fontlist = func_to_whole_process(config["filepath"], dir)
    print(check_func(fontlist, config["font_to_be"]))


if __name__ == "__main__":
    main()
