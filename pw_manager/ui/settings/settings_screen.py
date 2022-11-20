from pw_manager.utils import utils, constants

from pw_manager.ui.settings.color import color
from pw_manager.ui import db_sync_screen

from YeetsMenu.menu import Menu
from YeetsMenu.option import Option


def show():
    utils.clear_screen()

    menu = Menu(utils.get_noice_text("Settings"), colors=constants.colors)
    menu.add_selectable(Option("Color settings", color.show, skip_enter_confirmation=True))
    menu.add_selectable(Option("Database sync settings", db_sync_screen.show, skip_enter_confirmation=True))

    menu.run()
