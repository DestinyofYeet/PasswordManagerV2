import string

import stdiomask

from YeetsMenu.menu import Menu
from YeetsMenu.option import Option

from colorama import Style, Fore

import pw_manager.db
from pw_manager.utils import utils, constants
from pw_manager.utils import decorators
from pw_manager.db_entry import DatabaseEntry


@decorators.require_valid_db
def search_entry():
    def show_entry(entry_to_show: DatabaseEntry, show_password: bool = False):
        utils.clear_screen()
        print(f"{Fore.MAGENTA}Website or usage: {Fore.CYAN}{entry_to_show.website_or_usage}")
        print(f"{Fore.MAGENTA}Username: {Fore.CYAN}{entry_to_show.username}")
        print(f"{Fore.MAGENTA}Description: {Fore.CYAN}{entry_to_show.description}")
        print(f"{Fore.MAGENTA}Password: {Fore.CYAN}{len(entry_to_show.password) * '*' if not show_password else entry_to_show.password}")
        utils.reset_style()

        if not show_password:
            print()
            if input(f"{Fore.MAGENTA}Show password? y/n: {Fore.CYAN}").lower() == "y":
                utils.reset_style()
                show_entry(entry_to_show, True)
            else:
                utils.reset_style()

        print()
        if not show_password:
            utils.enter_confirmation()

    while True:
        utils.clear_screen()
        utils.print_noice("Search entry")

        db: pw_manager.db.Database = constants.db_file

        entries: list[DatabaseEntry] = db.get_all_entries()

        entries.sort()

        i: int = 1

        print(f"{Fore.CYAN}0{Fore.MAGENTA}) {Fore.CYAN}Exit this menu{Style.RESET_ALL}")

        for entry in entries:
            print(f"{Fore.CYAN}{i}{Fore.MAGENTA}) {Fore.CYAN if i % 2 == 0 else Fore.MAGENTA}{entry.website_or_usage}{Style.RESET_ALL}")
            i += 1

        print()
        user_input = utils.ask_till_input(f"{Fore.MAGENTA}Enter a number or a term to search for\n > {Fore.CYAN}")
        utils.reset_style()

        is_number: bool = False

        try:
            user_input = int(user_input)
            is_number = True
        except ValueError:
            pass

        if is_number:
            if user_input == 0:
                return

            if user_input > len(entries):
                print(f"{Fore.RED}The number is greater than the number of entries!{Style.RESET_ALL}")
                continue

            selected_entry = entries[user_input - 1]

            show_entry(selected_entry)

        else:
            result_list = []

            for entry in entries:

                if user_input.lower() in entry.website_or_usage.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.username.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.description.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.password.lower():
                    result_list.append(entry)

            menu = Menu(utils.get_noice_text(f"Search result for \"{user_input}\""))

            for entry in result_list:
                menu.add_selectable(Option(entry.website_or_usage, show_entry, entry, skip_enter_confirmation=True))

            menu.run()


@decorators.require_valid_db
def add_entry(provided_password: str = ""):
    utils.clear_screen()
    utils.print_noice("Add entry")

    try:
        website_or_usage = utils.ask_till_input(f"{Fore.MAGENTA}Please enter the website or usage of this entry.\n > {Fore.CYAN}")
        username = input(f"{Fore.MAGENTA}Please enter the username of this entry. (Can be left empty)\n > {Fore.CYAN}")
        description = input(f"{Fore.MAGENTA}Please enter the description of this entry. (Can be left empty)\n > {Fore.CYAN}")

        password = ""

        if provided_password:
            if utils.ask_till_input(f"{Fore.MAGENTA}A password from the password generator has been detected, do you want to use it? y/N\n > {Fore.CYAN}").lower() == "y":
                password = provided_password

        if not password:
            while True:
                password = utils.ask_till_input_secret(f"{Fore.MAGENTA}Please enter the password of this entry.\n > {Fore.CYAN}")
                password_confirmation = utils.ask_till_input_secret(f"{Fore.MAGENTA}Please confirm your password.\n > {Fore.CYAN}")

                if password != password_confirmation:
                    yes_no = utils.ask_till_input(f"{Fore.RED}Passwords do not match! Do you want to re-enter them? y/n\n > {Fore.CYAN}")

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


@decorators.require_valid_db
def modify_entry():
    utils.clear_screen()
    utils.print_noice("Modify entry")

    def real_modify_entry(entry_to_show: DatabaseEntry, show_password: bool = False):
        utils.clear_screen()
        utils.print_noice("Old entry")
        print(f"{Fore.MAGENTA}Website or usage: {Fore.CYAN}{entry_to_show.website_or_usage}")
        print(f"{Fore.MAGENTA}Username: {Fore.CYAN}{entry_to_show.username}")
        print(f"{Fore.MAGENTA}Description: {Fore.CYAN}{entry_to_show.description}")
        print(
            f"{Fore.MAGENTA}Password: {Fore.CYAN}{len(entry_to_show.password) * '*' if not show_password else entry_to_show.password}")

        print()

        utils.print_noice("Modify entry")

        new_website_or_usage = input(f"{Fore.MAGENTA}Please enter a new website or usage! (Leave blank for no change)\n > {Fore.CYAN}")
        new_username = input(f"{Fore.MAGENTA}Please enter a new username! (Leave blank for no change)\n > {Fore.CYAN}")
        new_description = input(f"{Fore.MAGENTA}Please enter a new description! (Leave blank for no change)\n > {Fore.CYAN}")
        new_password = stdiomask.getpass(f"{Fore.MAGENTA}Please enter a new password! (Leave blank for no change)\n > {Fore.CYAN}")

        new_entry = DatabaseEntry(website_or_usage=entry_to_show.website_or_usage, username=entry_to_show.username, description=entry_to_show.description, password=entry_to_show.password)

        if new_website_or_usage:
            if utils.ask_till_input(f"{Fore.MAGENTA}Are you sure you want to update the website or usage? y/N \n > {Fore.CYAN}").lower() == "y":
                new_entry.website_or_usage = new_website_or_usage
                print(f"{Fore.GREEN}Updated website or usage!{Style.RESET_ALL}")

        if new_username:
            if utils.ask_till_input(f"{Fore.MAGENTA}Are you sure you want to update the username? y/N\n > {Fore.CYAN}").lower() == "y":
                new_entry.username = new_username
                print(f"{Fore.GREEN}Updated username!{Style.RESET_ALL}")

        if new_description:
            if utils.ask_till_input(f"{Fore.MAGENTA}Are you sure you want to update the description? y/N\n > {Fore.CYAN}").lower() == "y":
                new_entry.description = new_description

        if new_password:
            while True:
                password_confirm = utils.ask_till_input_secret(f"{Fore.MAGENTA}Please confirm your new password!\n > {Fore.CYAN}")

                if new_password != password_confirm:
                    print(f"{Fore.RED}Passwords don't match! Please try again!")
                else:
                    break

            if utils.ask_till_input(f"{Fore.MAGENTA}Are you sure you want to update the password? y/N\n > {Fore.CYAN}").lower() == "y":
                new_entry.password = new_password

        db.update_entry(old_entry=entry_to_show, new_entry=new_entry)

        utils.reset_style()

    while True:
        utils.clear_screen()
        utils.print_noice("Search entry")

        db: pw_manager.db.Database = constants.db_file

        entries: list[DatabaseEntry] = db.get_all_entries()

        entries.sort()

        i: int = 1

        print(f"{Fore.CYAN}0{Fore.MAGENTA}) {Fore.CYAN}Exit this menu{Style.RESET_ALL}")

        for entry in entries:
            print(f"{Fore.CYAN}{i}{Fore.MAGENTA}) {Fore.CYAN if i % 2 == 0 else Fore.MAGENTA}{entry.website_or_usage}{Style.RESET_ALL}")
            i += 1

        print()
        user_input = utils.ask_till_input(f"{Fore.MAGENTA}Enter a number or a term to search for\n > {Fore.CYAN}")
        utils.reset_style()

        is_number: bool = False

        try:
            user_input = int(user_input)
            is_number = True
        except ValueError:
            pass

        if is_number:
            if user_input == 0:
                return

            if user_input > len(entries):
                print(f"{Fore.RED}The number is greater than the number of entries!{Style.RESET_ALL}")
                continue

            selected_entry = entries[user_input - 1]

            real_modify_entry(selected_entry)

        else:
            result_list = []

            for entry in entries:

                if user_input.lower() in entry.website_or_usage.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.username.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.description.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.password.lower():
                    result_list.append(entry)

            menu = Menu(utils.get_noice_text(f"Search result for \"{user_input}\""))

            for entry in result_list:
                menu.add_selectable(Option(entry.website_or_usage, real_modify_entry, entry, skip_enter_confirmation=True))

            menu.run()


@decorators.require_valid_db
def password_generator():
    utils.clear_screen()
    utils.print_noice("Password generator")

    length_of_password: int = 0
    while length_of_password == 0:
        length = utils.ask_till_input(f"{Fore.MAGENTA}Enter the length of the password you want!\n > {Fore.CYAN}")
        utils.reset_style()
        try:
            length_of_password = int(length)
        except ValueError:
            print(f"{Fore.RED}Invalid input! Try again!")
            continue

    chars = []

    if utils.ask_till_input(f"{Fore.MAGENTA}Do you want to have lowercase characters? y/N\n > {Fore.CYAN}").lower() == "y":
        chars.append(string.ascii_lowercase)

    if utils.ask_till_input(f"{Fore.MAGENTA}Do you want to have uppercase characters? y/N\n > {Fore.CYAN}").lower() == "y":
        chars.append(string.ascii_uppercase)

    if utils.ask_till_input(f"{Fore.MAGENTA}Do you want to have digits? y/N\n > {Fore.CYAN}").lower() == "y":
        chars.append(string.digits)

    if utils.ask_till_input(f"{Fore.MAGENTA}Do you want to have symbols? y/N\n > {Fore.CYAN}").lower() == "y":
        chars.append(string.punctuation)

    utils.reset_style()

    password = utils.generate_password(length_of_password, chars)

    print()
    print(f"{Fore.MAGENTA}Here is you password: {Fore.CYAN}\n\n{password}")
    print()

    if utils.ask_till_input(f"{Fore.MAGENTA}Do you want to use this password to make an entry? y/N\n > {Fore.CYAN}").lower() == "y":
        add_entry(password)


def delete_entry():
    utils.clear_screen()
    utils.print_noice("Delete entry")

    def real_delete_entry(entry_to_show: DatabaseEntry, show_password: bool = False):
        utils.clear_screen()
        utils.print_noice("Entry to delete")
        print(f"{Fore.MAGENTA}Website or usage: {Fore.CYAN}{entry_to_show.website_or_usage}")
        print(f"{Fore.MAGENTA}Username: {Fore.CYAN}{entry_to_show.username}")
        print(f"{Fore.MAGENTA}Description: {Fore.CYAN}{entry_to_show.description}")
        print(
            f"{Fore.MAGENTA}Password: {Fore.CYAN}{len(entry_to_show.password) * '*' if not show_password else entry_to_show.password}")

        print()

        if utils.ask_till_input(f"{Fore.MAGENTA}Are you sure you want to delete this entry? y/N\n > {Fore.CYAN}").lower() == "y":
            db.delete_entry(entry_to_show)
            print(f"{Fore.GREEN}Successfully deleted the entry!{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}Did not delete the entry!{Style.RESET_ALL}")

        utils.enter_confirmation()

    while True:
        utils.clear_screen()
        utils.print_noice("Search entry")

        db: pw_manager.db.Database = constants.db_file

        entries: list[DatabaseEntry] = db.get_all_entries()

        entries.sort()

        i: int = 1

        print(f"{Fore.CYAN}0{Fore.MAGENTA}) {Fore.CYAN}Exit this menu{Style.RESET_ALL}")

        for entry in entries:
            print(
                f"{Fore.CYAN}{i}{Fore.MAGENTA}) {Fore.CYAN if i % 2 == 0 else Fore.MAGENTA}{entry.website_or_usage}{Style.RESET_ALL}")
            i += 1

        print()
        user_input = utils.ask_till_input(f"{Fore.MAGENTA}Enter a number or a term to search for\n > {Fore.CYAN}")
        utils.reset_style()

        is_number: bool = False

        try:
            user_input = int(user_input)
            is_number = True
        except ValueError:
            pass

        if is_number:
            if user_input == 0:
                return

            if user_input > len(entries):
                print(f"{Fore.RED}The number is greater than the number of entries!{Style.RESET_ALL}")
                continue

            selected_entry = entries[user_input - 1]

            real_delete_entry(selected_entry)

        else:
            result_list = []

            for entry in entries:

                if user_input.lower() in entry.website_or_usage.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.username.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.description.lower():
                    result_list.append(entry)

                elif user_input.lower() in entry.password.lower():
                    result_list.append(entry)

            menu = Menu(utils.get_noice_text(f"Search result for \"{user_input}\""))

            for entry in result_list:
                menu.add_selectable(
                    Option(entry.website_or_usage, real_delete_entry, entry))

            menu.run()


def show():
    utils.clear_screen()

    menu = Menu(utils.get_noice_text("Password menu"))

    menu.add_selectable(Option("Search an entry", search_entry, skip_enter_confirmation=True))
    menu.add_selectable(Option("Add an entry", add_entry))
    menu.add_selectable(Option("Modify an entry", modify_entry))
    menu.add_selectable(Option("Delete an entry", delete_entry))
    menu.add_selectable(Option("Password generator", password_generator))

    menu.run()
