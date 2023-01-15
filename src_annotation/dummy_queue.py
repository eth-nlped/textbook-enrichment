#!/usr/bin/env python3

import glob
import json
import os
import random

subsection = "science/biology_2e/2-2"
subsection = "science/biology_2e/2-3"
subsection = "science/univeristy_physics/1-4"
MODES=["retrievals_local", "retrievals_joint", "retrievals_global", "gold"]

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
    
for subsection in ["science/biology_2e/2-1"]:
    for mode in MODES:
    # mode = random.sample(MODES)
        subsection_texts = [
            f.removeprefix("src_annotation_ui/web/texts/") for f in
            glob.glob(f"src_annotation_ui/web/texts/{subsection}/*.htm")
            if "bdet" not in f and "lobj" not in f
        ]
        subsection_texts.sort(key=lambda x: int(x.split("-")[-1].removesuffix(".htm")))

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
            "subsection": subsection,
            "texts": subsection_texts,
            "imgs": imgs,
        }
        print(json.dumps(line_out))