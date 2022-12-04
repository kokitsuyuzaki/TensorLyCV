#!/bin/bash

# Data Download
wget --no-check-certificate https://figshare.com/ndownloader/files/38344040 \
-O data/vaccine_tensor.npy

# Perform tensorlycv
docker run ghcr.io/kokitsuyuzaki/tensorlycv:main \
-i data/vaccine_tensor.npy -o output \
--cores=2 --rank=2 --trials=2 --iters=2 \
--ratio=30 --memgb=100
