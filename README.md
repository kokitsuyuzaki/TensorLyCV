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
- Snakemake: v7.1.0
- Singularity: v3.8.0
- Docker: v20.10.7

# Usage

As a demonstration, here we apply [`TensorLy`](http://tensorly.org/stable/index.html) to the data from [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097) (questionnaire on adverse reactions to COVID-19 vaccine).

## Download data

In this workflow, the input data is assumed to be a `Numpy` three-dimensional array saved by `numpy.save`.
The vaccine tensor data can be downloaded as below.

```bash
wget --no-check-certificate https://figshare.com/ndownloader/files/38344040 \
-O data/vaccine_tensor.npy
```

## Example with local machine

Then, we perform this workflow by `snakemake` command as follows.

```bash
snakemake -j 2 --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=30 \
--resources mem_gb=10 --use-singularity
```

The meanings of all the arguments are below.

- `-j`: [Number of cores to use Snakemake](https://snakemake.readthedocs.io/en/stable/executing/cli.html#useful-command-line-arguments) (e.g. 10, mandatory)
- `--config`: [Snakemake option to set the configuration](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html) (mandatory)
- `input`: Input file (e.g., vaccine_tensor.npy)
- `outdir`: Output directory (e.g., output)
- `rank`: Maximum rank parameter to search (e.g., 10)
- `trials`: Number of random trials (e.g., 50)
- `iters`: Number of iterations (e.g., 1000)
- `ratio`: Sampling ratio of cross validation (0 - 100, e.g., 20)
- `--resources`: [Snakemake option to control resources](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#resources) (optional)
- `mem_gb`: Memory usage (GB, e.g. 10, optional)
- `--use-singularity`: Snakemake option to use `Singularity` (mandatory)

## Example with parallel environment (GridEngine)

If `GridEngine` (`qsub` command) is available in your environment, you can add the `qsub` command after the `--cluster` option. This allows jobs to be submitted to multiple nodes and the computations to be distributed.

```bash
snakemake -j 2 --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=30 \
--resources mem_gb=10 --use-singularity
--cluster "qsub -l nc=4 -p -50 -r yes"
```

## Example with parallel environment (Slurm)

Likewise, if `Slurm` (`sbatch` command) is available in your environment, you can add the `sbatch` command after the `--cluster` option.

```bash
snakemake -j 2 --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=30 \
--resources mem_gb=10 --use-singularity
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