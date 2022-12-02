# TensorLyCV

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.0.5-brightgreen.svg)](https://snakemake.github.io)
[![DOI](https://zenodo.org/badge/135140554.svg)](https://zenodo.org/badge/latestdoi/135140554)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/build_test_push.yml/badge.svg)

Cross validation workflow of TensorLy

This workflow consists of the rules below:

![](https://github.com/kokitsuyuzaki/TensorLyCV/blob/main/plot/dag.png?raw=true)

# Pre-requisites
- Docker: vX.XX.X

# Usage

[Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097)

## Download data

Numpy three-dimensional array saved by numpy.save()

```bash
wget --no-check-certificate https://figshare.com/ndownloader/files/38344040 \
-O vaccine_tensor.npy
```

## Minimum example with required arguments (local machine with Docker)

```bash
docker run -it --rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:latest -i /work/vaccine_tensor.npy -o /work/output
```

## Example with full optional arguments (local machine with Docker)

```bash
docker run -it --rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:latest \
-i /work/vaccine_tensor.npy -o /work/output \
--cores=10 --rank=10 --trials=50 --iters=1000 \
--ratio=30 --memgb=100
```

## Example with parallel environment (GridEngine)

```bash
docker run -it --rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:latest \
-i /work/vaccine_tensor.npy -o /work/output \
--cores=10 --rank=10 --trials=50 --iters=1000 \
--ratio=30 --memgb=100 \
--cluster="qsub -l nc=4 -p -50 -r yes"
```

## Example with parallel environment (Slurm)

```bash
docker run -it --rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:latest \
-i /work/vaccine_tensor.npy -o /work/output \
--cores=10 --rank=10 --trials=50 --iters=1000 \
--ratio=30 --memgb=100 \
--cluster="sbatch -n 4 --nice=50 --requeue"
```

# Reference
- [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097)
- [TensorLy](http://tensorly.org/stable/index.html)

# Authors
- Koki Tsuyuzaki
- Eiryo Kawakami