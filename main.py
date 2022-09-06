import sqlite3
from create_tables import *
from insert_tables import *
from select_tables import *


def help_me():
    menu = """Command format:
    ? - this help
    1 - creation of tables
    2 - completing tables
    3 - selections from tables
    . - exit the program"""
    print(menu)


def unknown_command():
    print('Unknown command! Enter again!\n')


COMMANDS = {create_tables: '1', insert_tables: '2', select_tables: '3', help_me: '?'}


def command_parser(user_command: str) -> None:
    for key, value in COMMANDS.items():
        if user_command.lower() == value:
            return key
    else:
        return unknown_command


if __name__ == '__main__':
    help_me()
    while True:
        user_command = input('Enter command >>> ')
        if user_command == '.':
            print('Good bye!')
            break
        command = command_parser(user_command)
        command()
