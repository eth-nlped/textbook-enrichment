#!/usr/bin/env python3

import glob
import json
import os

subsection = "science/biology_2e/2-1"
MODE="gold"
MODE="retrievals_local"
MODE="retrievals_global"
MODE="retrievals_joint"

subsection_texts = [
    f.removeprefix("src_annotation_ui/web/texts/") for f in
    glob.glob(f"src_annotation_ui/web/texts/{subsection}/*.htm")
    if "bdet" not in f and "lobj" not in f
]
subsection_texts.sort(key=lambda x: int(x.split("-")[-1].removesuffix(".htm")))

path_base = subsection_texts[0].split("/")[:-1]
path_base = "/".join(path_base)+ "/"+path_base[-1]
print(path_base)
subsection_texts = [path_base + "-lobj.htm", path_base + "-bdet.htm"] + subsection_texts

def check_img_exists(path):
    return os.path.exists("src_annotation_ui/web/images/"+path)

def try_find_image_retrieval(img):
    if check_img_exists(img + ".jpeg"):
        return img+".jpeg"
    elif check_img_exists(img + ".jpg"):
        return img+".jpg"
    else:
        return None

def try_find_image_gold(img):
    img = img.replace("-", "/", 1)
    *img_base, signature = img.split("/")
    img_base = "/".join(img_base)

    if signature.count("-") != 2:
        return None
    s1, s2, s3 = signature.split("-")
    # error on Janvijay's side probably
    img = img_base+"/"+f"{s1}.{s2}.{s1}.{s3}.jpeg"
    if check_img_exists(img):
        return img
    return None

def try_find_image(img):
    img_hyp = try_find_image_retrieval(img+"/pred/0")
    if img_hyp:
        return img_hyp
    img_hyp = try_find_image_gold(img)
    if img_hyp:
        return img_hyp
    return None
    
imgs = []
for line in subsection_texts:
    *chapter, section, secsubsec = line.removesuffix(".htm").split("/")
    
    img = f"{MODE}/{'/'.join(chapter)}-{secsubsec}"
    img = try_find_image(img)
    if img:
        imgs.append([img])
    else:
        imgs.append([])


line_out = {
    "subsection": subsection,
    "texts": subsection_texts,
    "imgs": imgs,
}
print(json.dumps(line_out))