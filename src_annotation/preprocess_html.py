#!/usr/bin/env python3

import argparse
import glob
import os
import re

args = argparse.ArgumentParser()
args.add_argument("--files", default="data/formatted_htmls/**/*.htm")
args.add_argument("--input-replace", default="data/formatted_htmls")
args.add_argument("--output-replace", default="src_annotation_ui/web/texts/")
args = args.parse_args()

BAD_RGSX = [
    r'<center>.*?</center>',
    r'<div class="image-box">.*?</div>',
    r'<script>.*?myFunction.*?</script>',
]
BAD_RGSX = [re.compile(x) for x in BAD_RGSX]

GOOD_STYLE = "<style> * { font-family: Roboto, Arial, Helvetica, sans-serif; text-align: justify; } </style>"

for fname in glob.glob(args.files, recursive=True):
    data = open(fname, "r").read()
    data = data.replace("\n", "|||")
    for bad_regex in BAD_RGSX:
        data = bad_regex.sub("", data)
    data = re.sub(r'<style>.*?</style>', GOOD_STYLE, data)
    data = re.sub(r"<b>Section URL:</b>.*?</a>", "<b>Section URL:</b> retracted", data)
    data = re.sub(r"\|\|\|\|\|\|", "|||", data)

    fname_clean = fname.replace(args.input_replace, args.output_replace)
    os.makedirs("/".join(fname_clean.split("/")[:-1]), exist_ok=True)

    data = data.replace("|||", "\n")
    open(fname_clean, "w").write(data)