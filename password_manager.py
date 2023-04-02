import pathlib

import colorama
import json

from pw_manager.ui import main_screen
from pw_manager.utils import utils, constants


def main():
    colorama.init()

    color_config_file = utils.get_data_folder() + "/colors.json"

    if pathlib.Path(color_config_file).exists():
        with open(color_config_file) as f:
            color_obj = json.load(f)

        try:
            constants.colors[0] = utils.get_color(color_obj["primary"])
        except SyntaxError: # failed to get correct color
            pass

        try:
            constants.colors[1] = utils.get_color(color_obj["secondary"])
        except SyntaxError:
            pass

    main_screen.show()
    utils.exit_pw_manager()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        utils.exit_pw_manager()
