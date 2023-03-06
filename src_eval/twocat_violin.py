#!/usr/bin/env python3

import collections
import glob
import json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.lines import Line2D

args = argparse.ArgumentParser()
args.add_argument("-c", "--categories", default="relevancy")
args = args.parse_args()

data = [json.loads(l) for f in glob.glob("data_eval/*.jsonl")
        for l in open(f, "r").readlines()]
data = [{"mode": x["mode"], "responses": x["responses"]} for x in data]

print(list(data[0]["responses"].values())[0].keys())

if args.categories == "relevancy":
    CATEGORY_1 = "l_local_relevancy"
    CATEGORY_2 = "l_global_relevant"
elif args.categories == "redundancy":
    CATEGORY_1 = "l_local_redundancy"
    CATEGORY_2 = "l_global_redundancy"
else:
    raise Exception(f"Unknown category {args.categories}")

data_modes_1 = collections.defaultdict(list)
data_modes_2 = collections.defaultdict(list)

ANSWER_TO_NUM = {
    "irrelevant": 1,
    "somewhat relevant": 2,
    "relevant": 3,
    "undecided": None,
    "yes": 1,
    "no": 2,
}

for line in data:
    data_modes_1[line["mode"]].append(
        [ANSWER_TO_NUM[x[CATEGORY_1]] for x in line["responses"].values()])
    data_modes_2[line["mode"]].append(
        [ANSWER_TO_NUM[x[CATEGORY_2]] for x in line["responses"].values()])

# filter None
data_modes_1 = {
    mode: [[v for v in values_local if v] for values_local in values]
    for mode, values in data_modes_1.items()
}
data_modes_2 = {
    mode: [[v for v in values_local if v] for values_local in values]
    for mode, values in data_modes_2.items()
}
data_modes_1 = {
    mode: [np.average(values_local) for values_local in values if values_local]
    for mode, values in data_modes_1.items()
}
data_modes_2 = {
    mode: [np.average(values_local) for values_local in values if values_local]
    for mode, values in data_modes_2.items()
}

# MODES = list(data_modes.keys())
MODES = ['gold', 'retrievals_global', 'retrievals_joint', 'retrievals_local']

print(data_modes_1)

plt.figure(figsize=(4, 2))

# Draf left part of violin
violin_parts_left = plt.violinplot(
    [data_modes_1[x] for x in MODES],
    showmeans=False,
    widths=0.9,
    showextrema=False,
)

for pc in violin_parts_left['bodies']:
    pc.set_facecolor("tab:red")
    pc.set_edgecolor('black')
    pc.set_linewidth(1.2)
    pc.set_alpha(0.75)
    pc.set_aa(True)

    # get the center
    m = np.mean(pc.get_paths()[0].vertices[:, 0])
    pc.get_paths()[0].vertices[:, 0] = np.clip(
        pc.get_paths()[0].vertices[:, 0],
        -np.inf, m
    )
# draw means manually
for pos, values in enumerate(data_modes_1.values()):
    plt.plot(
        [pos + 1, pos + 1.5],
        [np.average(values)] * 2,
        color="black"
    )

# Draf right part of violin
violin_parts_right = plt.violinplot(
    [data_modes_2[x] for x in MODES],
    showmeans=False,
    widths=0.9,
    showextrema=False,
)

for pc in violin_parts_right['bodies']:
    pc.set_facecolor("tab:blue")
    pc.set_edgecolor('black')
    pc.set_linewidth(1.2)
    pc.set_alpha(0.75)
    pc.set_aa(True)

    # get the center
    m = np.mean(pc.get_paths()[0].vertices[:, 0])
    pc.get_paths()[0].vertices[:, 0] = np.clip(
        pc.get_paths()[0].vertices[:, 0],
        m, np.inf
    )

# draw means manually
for pos, values in enumerate(data_modes_2.values()):
    plt.plot(
        [pos + 0.5, pos + 1],
        [np.average(values)] * 2,
        color="black"
    )

plt.xticks(
    range(1, len(MODES) + 1),
    [m.replace("retrievals_", "").capitalize() for m in MODES]
)

if args.categories == "relevancy":
    plt.yticks([1, 2, 3], ["Irrelevant", "Somewhat\nrelevant", "Relevant"])
elif args.categories == "redundancy":
    plt.yticks([1, 2], ["Redundant", "Not\nredundant"])


legend_lines = [
    Line2D([0], [0], lw=0, marker="s", color="tab:red", markeredgecolor="black"),
    Line2D([0], [0], lw=0, marker="s", color="tab:blue", markeredgecolor="black")]

if args.categories == "relevancy":
    plt.legend(
        legend_lines, ['Local', 'Global'],
        loc="lower left", ncol=1,
        borderpad=0.1,
        handletextpad=0.1,
    )

if args.categories == "relevancy":
    plt.tight_layout(pad=0.9)
    plt.savefig("computed/figures/violin_relevancy.pdf")
elif args.categories == "redundancy":
    plt.tight_layout(pad=0.9, rect=[0, 0, 1, 1])
    plt.savefig("computed/figures/violin_redundancy.pdf")


plt.show()
