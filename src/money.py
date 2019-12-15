from dao import Database
from display import Display
import os


def main():
    credentials = load_cached_credentials()
    if credentials is None:
        pass
    display = Display()
    database = Database()
    ting = 4


def load_cached_credentials():
    credentials = None
    #TODO
    return credentials


if __name__ == '__main__':
    main()