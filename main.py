#!/usr/bin/env python3

import json
import os
import pickle

import cv2
import numpy as np
import requests
from wofi import Wofi

SCRYFALL_URL = "https://api.scryfall.com/"
picker = Wofi()

# adding this ensures relative paths resolve correctly
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)


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

    json_file_payload = {"q": query}

    # store list of unique image ids
    img_ids = []
    while len(img_ids) < 10:
        r = requests.get(SCRYFALL_URL + "cards/random", params=json_file_payload)
        r_obj = json.loads(r.content)
        if r_obj["object"] == "error":
            print("Cannot pull cards from this set, choose another.")
            os._exit(1)
        if r_obj["id"] not in img_ids:
            img_ids.append(r_obj["id"])

    # Get border crop images for all unique cards in img_ids
    cv_imgs = []
    for i in range(len(img_ids)):
        image_file_payload = {"format": "image", "version": "border_crop"}
        r = requests.get(
            SCRYFALL_URL + f"cards/{img_ids[i]}", params=image_file_payload
        )
        filename = f"./images/card{i}"
        with open(filename, "wb") as f:
            f.write(r.content)
        cv_imgs.append(cv2.imread(filename))

    if any(img is None for img in cv_imgs):
        raise ValueError("One or more images failed to load")
    height, width = cv_imgs[0].shape[:2]
    cv_imgs = [cv2.resize(img, (width, height)) for img in cv_imgs]

    row1 = np.hstack(cv_imgs[0:5])
    row2 = np.hstack(cv_imgs[5:10])

    grid = np.vstack((row1, row2))

    cv2.imwrite("./images/grid.jpg", grid)

    # set the wallpaper with hyprctl
    os.system("mv ./images/grid.jpg ~/Wallpapers/wallpaper.jpg")
    os.system('hyprctl hyprpaper reload , contain:"~/Wallpapers/wallpaper.jpg"')


if __name__ == "__main__":
    main()
