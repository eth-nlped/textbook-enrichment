#!/usr/bin/env python3

import collections
import glob
import json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.lines import Line2D
import fig_utils


data = [
    [json.loads(l) for l in open(f, "r").readlines()]
    for f in glob.glob("data_eval/*.jsonl")
]
CATEGORIES = ['l_local_relevancy', 'l_local_redundancy', 'l_global_relevant', 'l_global_redundancy', 'l_global_useful']
data = [[x["responses"].values() for x in y] for y in data]

ANSWER_TO_NUM = {
    "irrelevant": 1,
    "somewhat relevant": 2,
    "relevant": 3,
    "undecided": None,
    "yes": 1,
    "no": 2,
}

plt.figure(figsize=(4,3))
for category in CATEGORIES:
    data_local = [
        [
            [ANSWER_TO_NUM[line[category]] for line in data_local[pos]]
            for data_local in data
            if len(data_local) > pos
        ]
        for pos in [0, 1, 2, 3]
    ]

    # filter None
    data_local = [
        [
            [x for x in line if x]
            for line in data_local[pos]
        ]
        for pos in [0, 1, 2, 3]
    ]
    # filter empty array
    data_local = [
        [
            np.average(line)
            for line in data_local[pos]
            if line
        ]
        for pos in [0, 1, 2, 3]
    ]

    plt.plot(
        [0,1,2,3],
        [np.average(data_local[pos]) for pos in [0,1,2,3]],
        marker=".",
        ms=20,
        label=category.replace("_", " ").removeprefix("l ").replace("relevant", "relevancy").replace("useful", "usefulness").capitalize(),
    )

plt.yticks([1.3, 2.6], ["Worse", "Better"])
plt.xticks(range(4), range(4))
plt.xlabel("Position in evaluation")
plt.legend(bbox_to_anchor=(-0.15, 1, 1.15, 0), loc="lower left", mode="expand", ncol=2)

plt.tight_layout(pad=0.5)
plt.savefig("computed/figures/evaluation_pos_effect.pdf")
plt.show()
