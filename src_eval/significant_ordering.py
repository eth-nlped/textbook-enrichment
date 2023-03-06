#!/usr/bin/env python3

import collections
import glob
import json
import numpy as np
import argparse
import fig_utils
import scipy.stats
from math import log10, floor

args = argparse.ArgumentParser()
args.add_argument("-c", "--categories", default="relevancy")
args = args.parse_args()

data = [json.loads(l) for f in glob.glob("data_eval/*.jsonl")
        for l in open(f, "r").readlines()]
data = [{"mode": x["mode"], "responses": x["responses"]} for x in data]


ANSWER_TO_NUM = {
    "irrelevant": 1,
    "somewhat relevant": 2,
    "relevant": 3,
    "undecided": None,
    "yes": 1,
    "no": 2,
}
CATEGORIES = ['l_local_relevancy', 'l_local_redundancy',
              'l_global_relevant', 'l_global_redundancy', 'l_global_useful']
PRETTY_NAME = {
    "gold": "Go",
    'retrievals_local': "L",
    'retrievals_joint': "J",
    'retrievals_global': "Gl",
}
# ugly hack because I don't know the proper formatting magic


def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))


for category in CATEGORIES:
    data_modes = collections.defaultdict(list)

    for line in data:
        data_modes[line["mode"]].append(
            [ANSWER_TO_NUM[x[category]] for x in line["responses"].values()]
        )

    # filter None
    data_modes = {
        mode: [[v for v in values_local if v] for values_local in values]
        for mode, values in data_modes.items()
    }
    data_modes = {
        mode: [np.average(values_local)
               for values_local in values if values_local]
        for mode, values in data_modes.items()
    }

    if category == "l_global_useful":
        data_modes = {mode: [4 - v for v in values]
                      for mode, values in data_modes.items()}

    modes = ['gold', 'retrievals_global',
             'retrievals_joint', 'retrievals_local']
    modes.sort(reverse=True, key=lambda x: np.average(data_modes[x]))

    pvals = []
    for modes_i in range(len(modes) - 1):
        values_1 = data_modes[modes[modes_i]]
        values_2 = data_modes[modes[modes_i + 1]]
        stats = scipy.stats.ttest_ind(
            values_1, values_2, alternative="greater",
            equal_var=False
        )[1]
        pvals.append(stats)

    output_line = (
        "$ \\text{" + PRETTY_NAME[modes[0]] + "} " +
        " ".join([">_{" f"{round(val, 3)}" "} \\text{" + PRETTY_NAME[mode] + "}" for val, mode in zip(pvals, modes[1:])]) +
        "$ \\\\"
    )
    output_line = (
        category.replace("_", " ").removeprefix("l ").replace("relevant", "relevancy").replace("useful", "usefulness").capitalize() +
        " & " + output_line
    )
    print(output_line)
