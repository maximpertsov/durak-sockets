import glob
import json
from copy import deepcopy
from itertools import chain

v1_inputs = glob.glob("tests/lib/durak/scenario_inputs/v1/**/input.json")
v1_outputs = glob.glob("tests/lib/durak/scenario_inputs/v1/**/output.json")
v2_inputs = glob.glob("tests/lib/durak/scenario_inputs/v2/**/input.json")
v2_outputs = glob.glob("tests/lib/durak/scenario_inputs/v2/**/output.json")


def update(path):
    try:
        with open(path, "r") as f:
            d = json.load(f)

        # Transform data
        # ===========================================
        players = []
        for player in d["to_state"]["players"]:
            p = deepcopy(player)
            p["state"] = []
            if p["id"] in d["to_state"]["yielded"]:
                p["state"].append("yielded")
            players.append(p)

        d["to_state"]["players"] = players
        del d["to_state"]["yielded"]
        # ===========================================

        print(d)

        # with open(path, "w") as f:
        #     json.dump(d, f, indent=2, sort_keys=True)
        #     f.write("\n")
    except:
        print("skipping {}".format(path))


if __name__ == "__main__":
    for path in chain(v1_outputs, v2_outputs):
    # for path in chain(v2_inputs):
        update(path)
