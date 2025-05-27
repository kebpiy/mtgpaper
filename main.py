#!/usr/bin/env python3

import pickle

import cv2
import numpy as np
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


def pick_set() -> str:
    with open("sets.pickle", "rb") as f:
        sets = pickle.load(f)
    index, _ = picker.select("Pick a set", list(sets.values()))
    return list(sets.keys())[index]


def main():
    # enter a color you want all cards to contain
    chosen_color = pick_color()
    set_color = True
    if chosen_color == None:
        set_color = False

    # select a set to pull the random cards from
    chosen_set = pick_set()

    # format the query
    query = f"s:{chosen_set}"
    if set_color:
        query += f" c:{chosen_color}"

    payload = {"q": query, "format": "image", "version": "border_crop"}

    # make the request, and save images to files
    cv_imgs = []
    for i in range(8):
        r = requests.get(SCRYFALL_URL + "cards/random", params=payload)
        with open(f"./images/card{i}", "wb") as f:
            f.write(r.content)
        cv_imgs.append(cv2.imread(f"./images/card{i}"))

    if any(img is None for img in cv_imgs):
        raise ValueError("One or more images failed to load")
    height, width = cv_imgs[0].shape[:2]
    cv_imgs = [cv2.resize(img, (width, height)) for img in cv_imgs]

    row1 = np.hstack(cv_imgs[0:4])
    row2 = np.hstack(cv_imgs[4:8])

    grid = np.vstack((row1, row2))

    cv2.imwrite("./images/output.jpg", grid)

    # image now generated in ./images


if __name__ == "__main__":
    main()
