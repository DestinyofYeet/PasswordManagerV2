import pathlib

from pw_manager.utils import constants, utils

from colorama import Fore, Style


def require_valid_db(func):
    def inner(*args, **kwargs):
        if constants.db_file is None:
            print(f"{Fore.RED}You need to select a database first!{Style.RESET_ALL}")
            return

        else:
            func(*args, **kwargs)

    return inner


def require_valid_sync_config(func):
    def inner(*args, **kwargs):
        if not pathlib.Path(utils.get_sync_file()).exists():
            print(f"{Fore.RED}You need to setup your sync settings first!{Style.RESET_ALL}")
            return

        func(*args, **kwargs)

    return inner


def catch_ctrl_c(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            return

    return inner
