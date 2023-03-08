#!/usr/bin/env python3

import collections
import glob
import json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.lines import Line2D
import fig_utils
import matplotlib as mpl

data = [
    [json.loads(l) for l in open(f, "r").readlines()]
    for f in glob.glob("data_eval/*.jsonl")
]
CATEGORIES = [
    'l_local_relevancy',
    'l_global_relevant',
    'l_local_redundancy', 'l_global_redundancy', 'l_global_useful'
]
data_gold = [
    [x["responses"].values() for x in y if x["mode"] == "gold"]
    for y in data
]
data = [
    [x["responses"].values() for x in y if x["mode"] != "gold"]
    for y in data
]

# l_what_included

ANSWER_TO_NUM = {
    "irrelevant": 1,
    "somewhat relevant": 2,
    "relevant": 3,
    "undecided": None,
    "yes": 1,
    "no": 2,
}

data_types = collections.defaultdict(list)
data_types_gold = collections.defaultdict(list)

for line in data:
    for line_local in line:
        for line_local_local in line_local:
            for type_name, type_val in line_local_local["l_what_included"].items():
                if type_val == "ok":
                    data_types[type_name].append(line_local_local)

for line in data_gold:
    for line_local in line:
        for line_local_local in line_local:
            for type_name, type_val in line_local_local["l_what_included"].items():
                if type_val == "ok":
                    data_types_gold[type_name].append(line_local_local)

types_names = list(data_types.keys())
img = np.zeros((len(CATEGORIES), len(types_names)))

plt.figure(figsize=(4.5, 3))
ax = plt.gca()

cmap = mpl.cm.get_cmap("Greens").copy()
VMIN = 1.9
VMAX = 3

for category_i, category in enumerate(CATEGORIES):
    for type_i, (type_name, line) in enumerate(data_types.items()):
        val = np.average([
            ANSWER_TO_NUM[x[category]]
            for x in line if ANSWER_TO_NUM[x[category]]
        ])
        val_gold = [
            ANSWER_TO_NUM[x[category]]
            for x in data_types_gold[type_name] if ANSWER_TO_NUM[x[category]]
        ]
        override_gold = False
        if len(val_gold) <= 5:
            override_gold = True
        if not val_gold:
            override_gold = True
            val_gold = 2
        else:
            val_gold = np.average(val_gold)

        if category == "l_global_useful":
            val = 3 - val
            val_gold = 3 - val_gold
        if category in {'l_local_redundancy', 'l_global_redundancy', 'l_global_useful'}:
            val *= 1.5
            val_gold *= 1.5

        a_i = type_i
        s_i = category_i
        
        
        triangle = plt.Polygon(
            np.array([[a_i, s_i], [a_i + 1, s_i], [a_i, s_i + 1]]) - 0.5,
            # color input needs to be normalized
            # skip if gold does not have value
            color=cmap((val_gold - VMIN) / (VMAX - VMIN)) if not override_gold else "black"
        )
        ax.add_patch(triangle)
        plt.text(
            type_i+0.25, category_i+0.2,
            f"{abs(val-VMIN)/(VMAX-VMIN)*9:.0f}",
            va="center", ha="center",
            color = "white" if val > 2.7 else "black",
        )
        if not override_gold:
            plt.text(
                type_i-0.25, category_i-0.2,
                f"{abs(val_gold-VMIN)/(VMAX-VMIN)*9:.0f}",
                va="center", ha="center",
                color = "white" if val_gold > 2.7 else "black",
            )
        
        img[category_i, type_i] = val

plt.imshow(img, cmap=cmap, vmin=VMIN, vmax=VMAX, aspect=0.8, norm=None)


# add decoration
a_i = -1.5
s_i = 5.2
WIDTH=1.25
triangle = plt.Polygon(
    np.array([[a_i, s_i], [a_i + WIDTH, s_i], [a_i, s_i + WIDTH]]) - 0.5,
    clip_on=False,
    facecolor=cmap((3 - VMIN) / (VMAX - VMIN)),
    edgecolor="black"
)
ax.add_patch(triangle)
triangle = plt.Polygon(
    np.array([[a_i+WIDTH, s_i+WIDTH], [a_i + WIDTH, s_i], [a_i, s_i +WIDTH]]) - 0.5,
    clip_on=False,
    facecolor=cmap((2.5 - VMIN) / (VMAX - VMIN)),
    edgecolor="black"
)
ax.add_patch(triangle)
plt.text(
    a_i-0.15, s_i-0.2,
    "Gold",
    va="center", ha="center",
    color="white"
)
plt.text(
    a_i+0.35, s_i+0.4,
    "Auto.",
    va="center", ha="center"
)

plt.xticks(
    range(len(types_names)),
    [
        # ("\n\n" if i % 2 else "") + c.replace(" / ", " ").replace(" ", "\n").capitalize()
        c.replace(" / ", " ").replace(" ", "\n").capitalize()
        for i, c in enumerate(types_names)
    ],
    rotation=45
)
plt.yticks(
    range(len(CATEGORIES)),
    [
        category.replace("_", " ").removeprefix("l ").replace("relevant", "relevancy").replace("useful", "usefulness").capitalize().replace(" ", "\n")
        for category in CATEGORIES
    ]
)
plt.tight_layout(pad=0.3)
plt.savefig("computed/figures/image_type_rating.pdf")
plt.show()
