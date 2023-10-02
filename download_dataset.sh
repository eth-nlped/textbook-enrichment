#!/usr/bin/bash

mkdir -p data/
mkdir -p data/figures

wget "https://drive.google.com/uc?export=download&id=1i08nqQ3dYpz9sPIjj_0aXE2_5iKq_Bn6" -O data/openstax_dataset_v1.json

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1wtlh9TXBsRRYtHCO79LGm-DzQfKsqbm3' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1wtlh9TXBsRRYtHCO79LGm-DzQfKsqbm3" -O data/figures.tar.gz && rm -rf /tmp/cookies.txt

tar -xvzf data/figures.tar.gz -C data/figures