import json
import pickle

import requests

SCRYFALL_URL = "https://api.scryfall.com/"

# Gets a list of all MTG sets, and pickles them to 'sets.pickle'

r = requests.get(SCRYFALL_URL + "sets")
sets_json = json.loads(r.content)

# Dict `code : full name`
sets = {}
for s in sets_json["data"]:
    sets[s["code"]] = s["name"]

with open("sets.pickle", "wb") as f:
    pickle.dump(sets, f)
