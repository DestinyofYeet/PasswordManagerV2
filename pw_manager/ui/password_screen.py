import string

import stdiomask

from YeetsMenu.menu import Menu
from YeetsMenu.option import Option

from colorama import Style, Fore

import pw_manager.db
from pw_manager.utils import utils, constants
from pw_manager.utils import decorators
from pw_manager.db_entry import DatabaseEntry


@decorators.require_valid_db(enter_confirmation=True)
def search_entry():
    def show_entry(entry_to_show: DatabaseEntry, show_password: bool = False):
        utils.clear_screen()
        print(f"{constants.colors[1]}Website or usage: {constants.colors[0]}{entry_to_show.website_or_usage}")
        print(f"{constants.colors[1]}Username: {constants.colors[0]}{entry_to_show.username}")
        print(f"{constants.colors[1]}Description: {constants.colors[0]}{entry_to_show.description}")
        print(f"{constants.colors[1]}Password: {constants.colors[0]}{len(entry_to_show.password) * '*' if not show_password else entry_to_show.password}")
        utils.reset_style()

        if not show_password:
            print()
            if input(f"{constants.colors[1]}Show password? y/n: {constants.colors[0]}").lower() == "y":
                utils.reset_style()
                show_entry(entry_to_show, True)
            else:
                utils.reset_style()

        print()
        if not show_password:
            utils.enter_confirmation()

    utils.get_entry("Search entry", show_entry)


@decorators.require_valid_db(enter_confirmation=False)
def add_entry(provided_password: str = ""):
    utils.clear_screen()
    utils.print_noice("Add entry")

    try:
        website_or_usage = utils.ask_till_input(f"{constants.colors[1]}Please enter the website or usage of this entry.\n > {constants.colors[0]}")
        username = input(f"{constants.colors[1]}Please enter the username of this entry. (Can be left empty)\n > {constants.colors[0]}")
        description = input(f"{constants.colors[1]}Please enter the description of this entry. (Can be left empty)\n > {constants.colors[0]}")

        password = ""

        if provided_password:
            if utils.ask_till_input(f"{constants.colors[1]}A password from the password generator has been detected, do you want to use it? y/N\n > {constants.colors[0]}").lower() == "y":
                password = provided_password

        if not password:
            while True:
                password = utils.ask_till_input_secret(f"{constants.colors[1]}Please enter the password of this entry.\n > {constants.colors[0]}")
                password_confirmation = utils.ask_till_input_secret(f"{constants.colors[1]}Please confirm your password.\n > {constants.colors[0]}")

                if password != password_confirmation:
                    yes_no = utils.ask_till_input(f"{Fore.RED}Passwords do not match! Do you want to re-enter them? y/n\n > {constants.colors[0]}")

                    if yes_no.lower() == "n":
                        raise KeyboardInterrupt

                else:
                    break

    except KeyboardInterrupt:
        print(f"{Fore.RED}Creation aborted!{Style.RESET_ALL}")
        return

    db: pw_manager.db.Database = constants.db_file

    db.add_database_entry(website_or_usage=website_or_usage, description=description, username=username, password=password)

    print(f"{Fore.GREEN}Entry successfully added!{Style.RESET_ALL}")


@decorators.require_valid_db(enter_confirmation=True)
def modify_entry():
    utils.clear_screen()
    utils.print_noice("Modify entry")

    def real_modify_entry(entry_to_show: DatabaseEntry, show_password: bool = False):
        utils.clear_screen()
        utils.print_noice("Old entry")
        print(f"{constants.colors[1]}Website or usage: {constants.colors[0]}{entry_to_show.website_or_usage}")
        print(f"{constants.colors[1]}Username: {constants.colors[0]}{entry_to_show.username}")
        print(f"{constants.colors[1]}Description: {constants.colors[0]}{entry_to_show.description}")
        print(
            f"{constants.colors[1]}Password: {constants.colors[0]}{len(entry_to_show.password) * '*' if not show_password else entry_to_show.password}")

        print()

        utils.print_noice("Modify entry")

        new_website_or_usage = input(f"{constants.colors[1]}Please enter a new website or usage! (Leave blank for no change)\n > {constants.colors[0]}")
        new_username = input(f"{constants.colors[1]}Please enter a new username! (Leave blank for no change)\n > {constants.colors[0]}")
        new_description = input(f"{constants.colors[1]}Please enter a new description! (Leave blank for no change)\n > {constants.colors[0]}")
        new_password = stdiomask.getpass(f"{constants.colors[1]}Please enter a new password! (Leave blank for no change)\n > {constants.colors[0]}")

        new_entry = DatabaseEntry(website_or_usage=entry_to_show.website_or_usage, username=entry_to_show.username, description=entry_to_show.description, password=entry_to_show.password)

        if new_website_or_usage:
            if utils.ask_till_input(f"{constants.colors[1]}Are you sure you want to update the website or usage? y/N \n > {constants.colors[0]}").lower() == "y":
                new_entry.website_or_usage = new_website_or_usage
                print(f"{Fore.GREEN}Updated website or usage!{Style.RESET_ALL}")

        if new_username:
            if utils.ask_till_input(f"{constants.colors[1]}Are you sure you want to update the username? y/N\n > {constants.colors[0]}").lower() == "y":
                new_entry.username = new_username
                print(f"{Fore.GREEN}Updated username!{Style.RESET_ALL}")

        if new_description:
            if utils.ask_till_input(f"{constants.colors[1]}Are you sure you want to update the description? y/N\n > {constants.colors[0]}").lower() == "y":
                new_entry.description = new_description
                print(f"{Fore.GREEN}Updated description!{Style.RESET_ALL}")

        if new_password:
            while True:
                password_confirm = utils.ask_till_input_secret(f"{constants.colors[1]}Please confirm your new password!\n > {constants.colors[0]}")

                if new_password != password_confirm:
                    print(f"{Fore.RED}Passwords don't match! Please try again!")
                else:
                    break

            if utils.ask_till_input(f"{constants.colors[1]}Are you sure you want to update the password? y/N\n > {constants.colors[0]}").lower() == "y":
                new_entry.password = new_password
                print(f"{Fore.GREEN}Updated password!{Style.RESET_ALL}")

        constants.db_file.update_entry(old_entry=entry_to_show, new_entry=new_entry)

        utils.reset_style()

    utils.get_entry("Modify entry", real_modify_entry, skip_enter_confirmation=False)


def password_generator():
    utils.clear_screen()
    utils.print_noice("Password generator")

    length_of_password: int = 0
    while length_of_password == 0:
        length = utils.ask_till_input(f"{constants.colors[1]}Enter the length of the password you want!\n > {constants.colors[0]}")
        utils.reset_style()
        try:
            length_of_password = int(length)
        except ValueError:
            print(f"{Fore.RED}Invalid input! Try again!")
            continue

    chars = []

    if utils.ask_till_input(f"{constants.colors[1]}Do you want to have lowercase characters? y/N\n > {constants.colors[0]}").lower() == "y":
        chars.append(string.ascii_lowercase)

    if utils.ask_till_input(f"{constants.colors[1]}Do you want to have uppercase characters? y/N\n > {constants.colors[0]}").lower() == "y":
        chars.append(string.ascii_uppercase)

    if utils.ask_till_input(f"{constants.colors[1]}Do you want to have digits? y/N\n > {constants.colors[0]}").lower() == "y":
        chars.append(string.digits)

    if utils.ask_till_input(f"{constants.colors[1]}Do you want to have symbols? y/N\n > {constants.colors[0]}").lower() == "y":
        chars.append(string.punctuation)

    utils.reset_style()

    password = utils.generate_password(length_of_password, chars)

    print()
    print(f"{constants.colors[1]}Here is you password: {constants.colors[0]}\n\n{password}")
    print()

    if constants.db_file is not None:
        if utils.ask_till_input(f"{constants.colors[1]}Do you want to use this password to make an entry? y/N\n > {constants.colors[0]}").lower() == "y":
            add_entry(password)


def delete_entry():
    utils.clear_screen()
    utils.print_noice("Delete entry")

    def real_delete_entry(entry_to_show: DatabaseEntry, show_password: bool = False):
        utils.clear_screen()
        utils.print_noice("Entry to delete")
        print(f"{constants.colors[1]}Website or usage: {constants.colors[0]}{entry_to_show.website_or_usage}")
        print(f"{constants.colors[1]}Username: {constants.colors[0]}{entry_to_show.username}")
        print(f"{constants.colors[1]}Description: {constants.colors[0]}{entry_to_show.description}")
        print(
            f"{constants.colors[1]}Password: {constants.colors[0]}{len(entry_to_show.password) * '*' if not show_password else entry_to_show.password}")

        print()

        if utils.ask_till_input(f"{constants.colors[1]}Are you sure you want to delete this entry? y/N\n > {constants.colors[0]}").lower() == "y":
            constants.db_file.delete_entry(entry_to_show)
            print(f"{Fore.GREEN}Successfully deleted the entry!{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}Did not delete the entry!{Style.RESET_ALL}")

        utils.enter_confirmation()

    utils.get_entry("Delete entry", real_delete_entry, skip_enter_confirmation=True)


def show():
    utils.clear_screen()

    menu = Menu(utils.get_noice_text("Password menu"), constants.colors)

    menu.add_selectable(Option("Search an entry", search_entry, skip_enter_confirmation=True))
    menu.add_selectable(Option("Add an entry", add_entry))
    menu.add_selectable(Option("Modify an entry", modify_entry, skip_enter_confirmation=True))
    menu.add_selectable(Option("Delete an entry", delete_entry, skip_enter_confirmation=True))
    menu.add_selectable(Option("Password generator", password_generator))

    menu.run()
