#!/bin/bash

# Perform tensorlycv
docker run --rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:main \
-i /work/data/vaccine_tensor.npy -o /work/output \
--cores=2 --rank=2 --trials=2 --iters=2 \
--ratio=30 --memgb=100
