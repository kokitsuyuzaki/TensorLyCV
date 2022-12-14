# TensorLyCV

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.0.5-brightgreen.svg)](https://snakemake.github.io)
[![DOI](https://zenodo.org/badge/571380791.svg)](https://zenodo.org/badge/latestdoi/571380791)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/build_test_push.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun1.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun2.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun3.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/tensorlycv.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/release-please.yml/badge.svg)

Cross validation workflow of `TensorLy`

`TensorLyCV` consists of the rules below:

![](https://github.com/kokitsuyuzaki/TensorLyCV/blob/main/plot/dag.png?raw=true)

# Pre-requisites (our experiment)
- Bash: GNU bash, version 4.2.46(1)-release (x86_64-redhat-linux-gnu)
- Snakemake: v7.1.0
- Singularity: v3.8.0
- Docker: v20.10.7

# Usage

In this demo, we use the data from [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097) (questionnaire on adverse reactions to COVID-19 vaccine) but user can specify any user's higher-order array or tensor.

## Download this GitHub repository

First, download this GitHub repository and change the working directory.

```bash
git clone https://github.com/kokitsuyuzaki/TensorLyCV.git
cd TensorLyCV
```

## Download data

In `TensorLyCV`, the input data is assumed to be a `Numpy` three-dimensional array saved by `numpy.save`.
The vaccine tensor data can be downloaded as below.

```bash
wget --no-check-certificate https://figshare.com/ndownloader/files/38344040 \
-O data/vaccine_tensor.npy
```

## Example with local machine

Next, perform `tensorlycv` command as follows.

```bash
./tensorlycv -i data/vaccine_tensor.npy -o output \
--cores=2 --rank=2 --trials=2 --iters=2 \
--ratio=30 --memgb=100
```

The meanings of all the arguments are below.

- `-i` or `--input`: Input file (e.g., data/vaccine_tensor.npy, mandatory)
- `-o` or `--outdir`: Output directory (e.g., output, mandatory)
- `-c` or `--cores`: Number of cores used in Snakemake (e.g., default values is 10, optional)
- `-r` or `--rank`: Maximum rank parameter to search (e.g., default value is 10, optional)
- `-t` or `––trials`: Number of random trials (e.g., default value is 50, optional)
- `-e` or `--iters`: Number of iterations (e.g., default value is 1000, optional)
- `-a` or `--ratio`: Sampling ratio of cross validation (0 - 100, e.g., default value is 20, optional)
- `-m` or `--memgb`: Memory usage (GB, e.g. default value is 10, optional)
- `-l` or `--cluster`: Cluster option of Snakemake (e.g., "qsub -l nc=4 -p -50 -r yes", optional)
- `-h` or `--help`: Display help
- `-v` or `--version`: Version of this workflow


## Example with parallel environment (GridEngine)

If `GridEngine` (`qsub` command) is available in your environment, you can add the `qsub` command. Just adding the `--cluster` option, the jobs are submitted to multiple nodes and the computations are distributed.

```bash
./tensorlycv -i data/vaccine_tensor.npy -o output \
--cores=2 --rank=2 --trials=2 --iters=2 \
--ratio=30 --memgb=100 \
--cluster "qsub -l nc=4 -p -50 -r yes"
```

## Example with parallel environment (Slurm)

Likewise, if `Slurm` (`sbatch` command) is available in your environment, you can add the `sbatch` command after the `--cluster` option.

```bash
./tensorlycv -i data/vaccine_tensor.npy -o output \
--cores=2 --rank=2 --trials=2 --iters=2 \
--ratio=30 --memgb=100 \
--cluster "sbatch -n 4 --nice=50 --requeue"
```

## Example with local machine with Docker

If `docker` command is available, the following command can be performed without installing any tools.

```bash
docker run --rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:main \
-i /work/data/vaccine_tensor.npy -o /work/output \
--cores=2 --rank=2 --trials=2 --iters=2 \
--ratio=30 --memgb=100
```

# Reference
- [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097)
- [TensorLy](http://tensorly.org/stable/index.html)

# Authors
- Koki Tsuyuzaki
- Eiryo Kawakami