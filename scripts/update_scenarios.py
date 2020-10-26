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
        del d["to_state"]["collector"]
        # ===========================================

        print(d)

        # with open(path, "w") as f:
        #     json.dump(d, f, indent=2, sort_keys=True)
        #     f.write("\n")
    except:
        print("skipping {}".format(path))


if __name__ == "__main__":
    # for path in chain(v2_inputs):
    for path in chain(v1_outputs, v2_outputs):
        update(path)
