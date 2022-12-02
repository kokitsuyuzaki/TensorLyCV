# TensorLyCV

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.0.5-brightgreen.svg)](https://snakemake.github.io)
[![DOI](https://zenodo.org/badge/135140554.svg)](https://zenodo.org/badge/latestdoi/135140554)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/unittest.yml/badge.svg)

Cross validation workflow of TensorLy

This workflow consists of the rules below:

![](https://github.com/kokitsuyuzaki/TensorLyCV/blob/main/plot/dag.png?raw=true)

# Pre-requisites
- Bash: GNU bash, version 4.2.46(1)-release (x86_64-redhat-linux-gnu)
- Snakemake: 6.0.5
- Singularity: 3.5.3

# Usage

[Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097)

## Download this repository

Firstly, download this repository by git clone and change the working directory like below.

```bash
git clone https://github.com/kokitsuyuzaki/TensorLyCV.git
cd TensorLyCV
```

## Download data



Numpy three-dimensional array saved by numpy.save()


```bash
wget --no-check-certificate https://figshare.com/ndownloader/files/38344040 \
-O data/vaccine_tensor.npy
```

## Minimum example with required arguments (local machine)

The required arguments are `input` and `outdir`

```bash
snakemake -j 10 --config input=data/vaccine_tensor.npy outdir=output \
--use-singularity
```

## Example with full optional arguments (local machine)

```bash
snakemake -j 10 --config input=data/vaccine_tensor.npy outdir=output \
rank=10 trials=50 iters=1000 ratio=30 --resources mem_gb=100 \
--use-singularity
```

## Example with parallel environment (GridEngine)

```bash
snakemake -j 32 --config input=data/vaccine_tensor.npy outdir=output \
rank=10 trials=50 iters=1000 ratio=30 --resources mem_gb=100 \
--use-singularity \
--cluster "qsub -l nc=4 -p -50 -r yes" --latency-wait 60
```

## Example with parallel environment (Slurm)

```bash
snakemake -j 32 --config input=data/vaccine_tensor.npy outdir=output \
rank=10 trials=50 iters=1000 ratio=30 --resources mem_gb=100 \
--use-singularity \
--cluster "sbatch -n 4 --nice=50 --requeue" --latency-wait 60
```

# Reference
- [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097)
- [TensorLy](http://tensorly.org/stable/index.html)

# Authors
- Koki Tsuyuzaki
- Eiryo Kawakami