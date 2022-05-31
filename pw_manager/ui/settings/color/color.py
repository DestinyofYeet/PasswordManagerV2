import json
import pathlib

from pw_manager.utils import utils, constants

from YeetsMenu.menu import Menu
from YeetsMenu.option import Option
from colorama import Style, Fore


def select_color() -> str:
    while True:
        utils.clear_screen()

        color_map = {}

        print(f"{constants.colors[0]}0{constants.colors[1]}) {constants.colors[0]}Exit this menu{Style.RESET_ALL}")

        for color in constants.available_colors:
            color_map[len(color_map) + 1] = color

        for key, value in color_map.items():
            print(f"{constants.colors[0]}{key}{Fore.LIGHTMAGENTA_EX}) {utils.get_color(value)}{value}")

        selection = input(f"{Fore.LIGHTMAGENTA_EX}Please enter a number (Press enter without inputting anything for no change)!\n {constants.colors[0]}> ")
        utils.clear_screen()
        if not selection:
            return None

        try:
            selection = int(selection)
        except ValueError:
            print(f"{Fore.RED}Not a number!")
            utils.reset_style()
            utils.enter_confirmation()
            continue

        return color_map.get(selection)


def change_color():
    utils.clear_screen()
    utils.print_noice("Change colors")
    print(f"{constants.colors[1]}Press enter to change the primary color!")

    utils.reset_style()
    utils.enter_confirmation()
    primary_color = select_color()

    utils.clear_screen()
    utils.reset_style()

    print(f"{constants.colors[1]}Press enter to change the secondary color!")
    utils.reset_style()
    utils.enter_confirmation()
    secondary_color = select_color()

    colors_path = utils.get_data_folder() + "/colors.json"

    color_obj = {}

    if primary_color is not None:
        print(
            f"{Fore.GREEN}Changed the primary color from {constants.colors[0]}this color {Fore.GREEN}to {utils.get_color(primary_color)}{primary_color}{Fore.GREEN}!")

        constants.colors[0] = utils.get_color(primary_color)
        color_obj["primary"] = primary_color

    else:
        print(f"{Fore.GREEN}Primary color not changed!")

    if secondary_color is not None:
        print(
            f"{Fore.GREEN}Changed the secondary color from {constants.colors[1]}this color {Fore.GREEN}to {utils.get_color(secondary_color)}{secondary_color}{Fore.GREEN}!")

        constants.colors[1] = utils.get_color(secondary_color)
        color_obj["secondary"] = secondary_color

    else:
        print(f"{Fore.GREEN}Secondary color not changed!")

    utils.reset_style()

    if pathlib.Path(colors_path).exists():

        with open(colors_path) as f:
            file: dict = json.load(f)

        if file.get("primary") is not None and color_obj.get("primary") is not None:
            if file.get("primary") != color_obj.get("primary"):
                file["primary"] = color_obj.get("primary")

        if file.get("secondary") is not None and color_obj.get("secondary") is not None:
            if file.get("secondary") != color_obj.get("secondary"):
                file["secondary"] = color_obj.get("secondary")

        with open(colors_path, "w") as f:
            json.dump(file, f, indent=2)

    else:
        with open(colors_path, "w+") as f:
            json.dump(color_obj, f, indent=2)



def show():
    utils.clear_screen()

    menu = Menu(utils.get_noice_text("Color settings"), colors=constants.colors)
    menu.add_selectable(Option("Change colors", change_color))

    menu.run()
