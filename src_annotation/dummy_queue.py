#!/usr/bin/env python3

import glob
import json
import os
import random
import shutil

MODES=["retrievals_local", "retrievals_joint", "retrievals_global", "gold"]
SECTIONS = [
    'science/university_physics_1/11-1',
    'science/biology_2e/6-5',
    'business/entrepreneurship/2-2',
    'math/intermediate_algebra/3-2',
    'social_sciences/us_history/28-3',
    # 'social_sciences/american_government_3e/6-2',
]

random.seed(0)

def check_img_exists(path):
    return os.path.exists("src_annotation_ui/web/images/"+path)

def try_find_image_retrieval(img):
    if check_img_exists(img + ".jpeg"):
        return img+".jpeg"
    elif check_img_exists(img + ".jpg"):
        return img+".jpg"
    else:
        return None

def try_find_images_gold(path):
    imgs = []
    for i in range(10):
        img_hyp = try_find_image_retrieval("retrievals_local/"+ path +f"/gold/{i}")
        if not img_hyp:
            break
        imgs.append(img_hyp)
    return imgs

def try_find_images_retrieval(path):
    imgs = []
    for i in range(10):
        img_hyp = try_find_image_retrieval(path +f"/pred/{i}")
        if not img_hyp:
            break
        imgs.append(img_hyp)
    return imgs

for i in range(100):
    UID = f"prolific_pilot_1/s{i:0>2}"
# for UID in ["intertie", "epiphora"]:
    section_name = random.choice(SECTIONS)
    # for s_i, section_name in enumerate(SECTIONS):
    modes_local = list(MODES)
    random.shuffle(modes_local)
    lines_out = []
    for mode in modes_local:
    # mode = random.sample(MODES)
        subsection_texts = [
            f.removeprefix("src_annotation_ui/web/texts/") for f in
            glob.glob(f"src_annotation_ui/web/texts/{section_name}/*.htm")
            if "bdet" not in f and "lobj" not in f
        ]
        subsection_texts.sort(key=lambda x: int(x.split("-")[-1].removesuffix(".htm")))
        print(section_name, f"src_annotation_ui/web/texts/{section_name}/*.htm")
        
        path_base = subsection_texts[0].split("/")[:-1]
        path_base = "/".join(path_base)+ "/"+path_base[-1]
        subsection_texts = [path_base + "-lobj.htm", path_base + "-bdet.htm"] + subsection_texts

        imgs = []
        for line in subsection_texts:
            *chapter, section, secsubsec = line.removesuffix(".htm").split("/")
            if mode == "gold":
                imgs_local = try_find_images_gold('/'.join(chapter) + f"-{secsubsec}")
            else:
                path = f"{mode}/{'/'.join(chapter)}-{secsubsec}"
                imgs_local = try_find_images_retrieval(path)
            imgs.append(imgs_local)

        line_out = {
            "mode": mode,
            "subsection": section_name,
            "texts": subsection_texts,
            "imgs": imgs,
        }
        lines_out.append(line_out)
    with open(f"src_annotation_ui/web/queues/{UID}.jsonl", "w") as f:
        f.write("\n".join([json.dumps(x) for x in lines_out]))

# cleanup
for f in glob.glob("src_annotation_ui/web/texts/**", recursive=True):
    if f.count("/") == 5 and all(section not in f for section in SECTIONS):
        shutil.rmtree(f)

SECTION_STRIPS = [
    "/".join(section.split("/")[:-1]) + "-" + section.split("/")[-1]
    for section in SECTIONS
]
for mode in MODES:
    for f in glob.glob(f"src_annotation_ui/web/images/{mode}/**", recursive=True):
        if f.count("/") == 5 and all(section_strip not in f for section_strip in SECTION_STRIPS):
            shutil.rmtree(f)


# find src_annotation_ui/web/{images,texts} | xargs stat -c %s | awk '{ sum += $0 } END { if (sum) print sum/1000/1000 "M" }'