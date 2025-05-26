#!/usr/bin/env python3

import json

import requests
from wofi import Wofi

SCRYFALL_URL = "https://api.scryfall.com/"
picker = Wofi()


def pick_color() -> str | None:
    colors = ["Any", "White", "Blue", "Black", "Red", "Green"]
    index, _ = picker.select("Pick a color", colors)

    match index:
        case 0:
            color = None
        case 1:
            color = "w"
        case 2:
            color = "u"
        case 3:
            color = "b"
        case 4:
            color = "r"
        case 5:
            color = "g"
    return color


def pick_set() -> str | None:
    pass


def main():
    # enter a color you want all cards to contain
    color = pick_color()
    set_color = True
    if color == None:
        set_color = False

    # select a set to pull the random cards from


if __name__ == "__main__":
    main()
