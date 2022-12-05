# TensorLyCV

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.0.5-brightgreen.svg)](https://snakemake.github.io)
[![DOI](https://zenodo.org/badge/135140554.svg)](https://zenodo.org/badge/latestdoi/135140554)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/build_test_push.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun1.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun2.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun3.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/tensorlycv.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/release-please.yml/badge.svg)

Cross validation workflow of TensorLy

This workflow consists of the rules below:

![](https://github.com/kokitsuyuzaki/TensorLyCV/blob/main/plot/dag.png?raw=true)

# Pre-requisites (our experiment)
- Bash: GNU bash, version 4.2.46(1)-release (x86_64-redhat-linux-gnu)
- Snakemake: v6.0.5
- Singularity: v3.5.3
- Docker: v20.10.10

# Usage

As a demonstration, here we apply tensor decomposition to the data from [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097) (questionnaire on adverse reactions to COVID-19 vaccine).

## Download data

In this workflow, the input data is assumed to be a Numpy three-dimensional array saved by numpy.save().
The vaccine tensor data can be downloaded as below.

```bash
wget --no-check-certificate https://figshare.com/ndownloader/files/38344040 \
-O data/vaccine_tensor.npy
```

## Example with local machine

```bash
snakemake -j 2 --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=30 \
--resources mem_gb=10 --use-singularity
```

## Example with parallel environment (GridEngine)

```bash
snakemake -j 2 --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=30 \
--resources mem_gb=10 --use-singularity
--cluster "qsub -l nc=4 -p -50 -r yes"
```

## Example with parallel environment (Slurm)

```bash
snakemake -j 2 --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=30 \
--resources mem_gb=10 --use-singularity
--cluster "sbatch -n 4 --nice=50 --requeue"
```




## Example with local machine with Docker

```bash
docker run -it --rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:main \
-i /work/vaccine_tensor.npy -o /work/output \
--cores=10 --rank=10 --trials=50 --iters=1000 \
--ratio=30 --memgb=100
```

# Reference
- [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097)
- [TensorLy](http://tensorly.org/stable/index.html)

# Authors
- Koki Tsuyuzaki
- Eiryo Kawakami