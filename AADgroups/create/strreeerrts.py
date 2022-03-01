import os
import json
import sys

with open(os.path.join(sys.path[0], "streetaddressdept.json")) as json_file:
    config = json.load(json_file)
    print(config["Rotorua/EBOP"])