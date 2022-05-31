from colorama import Fore

db_file = None

available_colors = [i for i in dir(Fore) if not i.startswith("_")]

# colors = [Fore.WHITE, "\033[1;36;40m"]
colors = [Fore.CYAN, Fore.MAGENTA]
