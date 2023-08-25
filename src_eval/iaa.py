#!/usr/bin/env python3

import glob
import json
import collections
import numpy as np
import re

print(len([
    f for f in glob.glob("data/prolific_pilot_1/*.jsonl")
    if re.match(r".*s\d+.jsonl", f)
]))

data = [
    json.loads(line)
    for f in glob.glob("data/prolific_pilot_1/*.jsonl")
    if re.match(r".*s\d+.jsonl", f)
    for line in open(f, "r")
]
data_us = [
    json.loads(line)
    for f in glob.glob("data/prolific_pilot_1/*.jsonl")
    if re.match(r".*woudy-.*.jsonl", f)
    for line in open(f, "r")
]


def get_answer_score(answer):
    return {
        "no": 0,
        "undecided": 0.5,
        "yes": 1,
        "irrelevant": 0,
        "somewhat relevant": 0.5,
        "relevant": 1,
        "undecided": 0.5,
    }[answer]


print(len(data), "user lines")

data_groupped = collections.defaultdict(list)
for line in data:
    for img_key in line["responses"].keys():
        data_groupped[
            (line["subsection"], line["mode"], img_key)
        ].append(line["responses"][img_key])


exact_matches = []
vague_matches = []
for sig, values in data_groupped.items():
    if len(values) == 1:
        continue

    for p1_i, p1 in enumerate(values):
        for p2_i, p2 in enumerate(values[p1_i + 1:]):
            for key in p1.keys():
                if type(p1[key]) is dict:
                    continue
                v1 = get_answer_score(p1[key])
                v2 = get_answer_score(p2[key])
                vague_matches.append(abs(v1 - v2) == 0)
                exact_matches.append(abs(v1 - v2) != 1)


print(len(exact_matches), np.average(exact_matches), np.average(vague_matches))

exact_matches = []
vague_matches = []
for line in data_us:
    for img_key, p1 in line["responses"].items():
        for p2 in data_groupped[(line["subsection"], line["mode"], img_key)]:
            for key in p1.keys():
                if type(p1[key]) is dict:
                    continue
                v1 = get_answer_score(p1[key])
                v2 = get_answer_score(p2[key])
                vague_matches.append(abs(v1 - v2) == 0)
                exact_matches.append(abs(v1 - v2) != 1)
print(len(exact_matches), np.average(exact_matches), np.average(vague_matches))
