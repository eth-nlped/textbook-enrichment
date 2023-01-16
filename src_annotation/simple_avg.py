#!/usr/bin/env python3

import glob
import json
import collections
import numpy as np

# {"mode":"retrievals_joint","subsection":"social_sciences/us_history/28-3","texts":["social_sciences/us_history/28-3/28-3-lobj.htm","social_sciences/us_history/28-3/28-3-bdet.htm","social_sciences/us_history/28-3/28-3-1.htm","social_sciences/us_history/28-3/28-3-2.htm","social_sciences/us_history/28-3/28-3-3.htm","social_sciences/us_history/28-3/28-3-4.htm"],"imgs":[[],[],[],["retrievals_joint/social_sciences/us_history-28-3-2/pred/0.jpg","retrievals_joint/social_sciences/us_history-28-3-2/pred/1.jpg","retrievals_joint/social_sciences/us_history-28-3-2/pred/2.jpg"],["retrievals_joint/social_sciences/us_history-28-3-3/pred/0.jpg","retrievals_joint/social_sciences/us_history-28-3-3/pred/1.jpg"],[]],"start_time":1673903094336,"end_time":1673903331767,"responses":{"s_3_q_0":{"l_what_included":{"diagram / flowchart":"ok","graph / plot":"ok"},"l_local_relevancy":"irrelevant","l_local_redundancy":"no","l_global_relevant":"irrelevant","l_global_redundancy":"no","l_global_useful":"no"},"s_3_q_1":{"l_local_relevancy":"irrelevant","l_local_redundancy":"no","l_what_included":{"natural image":"ok"},"l_global_relevant":"irrelevant","l_global_redundancy":"no","l_global_useful":"no"},"s_3_q_2":{"l_local_relevancy":"relevant","l_local_redundancy":"no","l_what_included":{"natural image":"ok"},"l_global_relevant":"relevant","l_global_redundancy":"no","l_global_useful":"yes"},"s_4_q_0":{"l_local_relevancy":"irrelevant","l_local_redundancy":"no","l_what_included":{"natural image":"ok"},"l_global_relevant":"irrelevant","l_global_redundancy":"no","l_global_useful":"no"},"s_4_q_1":{"l_local_relevancy":"relevant","l_local_redundancy":"no","l_what_included":{"natural image":"ok"},"l_global_relevant":"relevant","l_global_useful":"yes","l_global_redundancy":"no"}}}

data = []
for f in glob.glob("src_annotation/prolific_pilot_1/*.jsonl"):
    with open(f, "r") as f:
        data += [json.loads(x) for x in f.readlines()]

print(len(data), "samples")

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


for metric in ["l_local_relevancy", "l_local_redundancy", "l_global_relevant", "l_global_redundancy", "l_global_useful"]:

    def get_subsection_score(subsection):
        return get_answer_score(subsection[metric])


    def get_line_score(line):
        return [
            get_subsection_score(subsection)
            for subsection in line["responses"].values()
        ]

    data_modes = collections.defaultdict(list)
    for line in data:
        data_modes[line["mode"]] += get_line_score(line)
    print("="*10)
    print(metric)
    for key, values in data_modes.items():
        values = [x for x in values if x]
        print(f"{key:>20}: {np.average(values):.1%}")
