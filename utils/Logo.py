from colorama import Fore
import os
def Logo():
     print(f"""{Fore.GREEN}
 _____         ____
|  ___|____  _|  _ \ __ _ ___ ___
| |_ / _ \ \/ / |_) / _` / __/ __|
|  _|  __/>  <|  __/ (_| \__ \__ |
|_|  \___/_/\_\_|   \__,_|___/___/
 {Fore.RED}by Dsevenfex
     """)

def Line():
     print(f"{Fore.GREEN}----------------------------------")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')