# TensorLyCV

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.0.5-brightgreen.svg)](https://snakemake.github.io)
[![DOI](https://zenodo.org/badge/571380791.svg)](https://zenodo.org/badge/latestdoi/571380791)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/build_test_push.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun1.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun2.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/dockerrun3.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/tensorlycv.yml/badge.svg)
![GitHub Actions](https://github.com/kokitsuyuzaki/TensorLyCV/actions/workflows/release-please.yml/badge.svg)

Cross-validation workflow of `TensorLy`

`TensorLyCV` consists of the rules below:

![](https://github.com/kokitsuyuzaki/TensorLyCV/blob/main/plot/dag.png?raw=true)

# Pre-requisites (our experiment)
- Snakemake: v7.1.0
- Singularity: v3.8.0
- Docker: v20.10.7 (optional)

`Snakemake` is available via Python package managers like `pip`, `conda`, or `mamba`.

`Singularity` and `Docker` are available by the installer provided in each website or package manager for each OS like `apt-get/yum` for Linux, or `brew` for Mac.

For the details, see the installation documents below.

- https://snakemake.readthedocs.io/en/stable/getting_started/installation.html
- https://docs.sylabs.io/guides/3.0/user-guide/installation.html
- https://docs.docker.com/engine/install/

**Note: The following source code does not work on M1/M2 Mac. M1/M2 Mac users should refer to [README_AppleSilicon.md](README_AppleSilicon.md) instead.**

# Usage

In this demo, we use the data from [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097) (questionnaire on adverse reactions to COVID-19 vaccine) but a user can specify any user's higher-order array or tensor.

## Download this GitHub repository

First, download this GitHub repository and change the working directory.

```bash
git clone https://github.com/kokitsuyuzaki/TensorLyCV.git
cd TensorLyCV
```

## Download data

In `TensorLyCV`, the input data is assumed to be a `Numpy` three-dimensional array saved by `numpy.save`.
The vaccine tensor data can be downloaded below.

```bash
mkdir -p data
wget --no-check-certificate https://figshare.com/ndownloader/files/38344040 \
-O data/vaccine_tensor.npy
```

## Example with local machine

Next, perform `TensorLyCV` by the `snakemake` command as follows.

**Note: To check if the command is executable, set smaller parameters such as rank_min=2 rank_max=2 trials=2 n_iter_max=2.**

```bash
snakemake -j 4 --config input=data/vaccine_tensor.npy outdir=output \
rank_min=1 rank_max=10 trials=50 n_iter_max=1000 ratio=30 \
--resources mem_gb=10 --use-singularity
```

The meanings of all the arguments are below.

- `-j`: Snakemake option to set [the number of cores](https://snakemake.readthedocs.io/en/stable/executing/cli.html#useful-command-line-arguments) (e.g. 10, mandatory)
- `--config`: Snakemake option to set [the configuration](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html) (mandatory)
- `input`: Input file (e.g., vaccine_tensor.npy, mandatory)
- `outdir`: Output directory (e.g., output, mandatory)
- `rank_min`: Lower limit of rank parameter to search (e.g., 1, mandatory)
- `rank_max`: Upper limit of rank parameter to search (e.g., 10, mandatory)
- `trials`: Number of random trials (e.g., 50, mandatory)
- `n_iter_max`: Number of iterations (e.g., 1000, mandatory)
- `ratio`: Sampling ratio of cross-validation (0 - 100, e.g., 30, mandatory)
- `--resources`: Snakemake option to control [resources](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#resources) (optional)
- `mem_gb`: Memory usage (GB, e.g. 10, optional)
- `--use-singularity`: Snakemake option to use Docker containers via [`Singularity`](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html) (mandatory)

## Example with the parallel environment (GridEngine)

If the `GridEngine` (`qsub` command) is available in your environment, you can add the `qsub` command. Just adding the `--cluster` option, the jobs are submitted to multiple nodes and the computations are distributed.

**Note: To check if the command is executable, set smaller parameters such as rank_min=2 rank_max=2 trials=2 n_iter_max=2.**

```bash
snakemake -j 32 --config input=data/vaccine_tensor.npy outdir=output \
rank_min=1 rank_max=10 trials=50 n_iter_max=1000 ratio=30 \
--resources mem_gb=100 --use-singularity \
--cluster "qsub -l nc=4 -p -50 -r yes" --latency-wait 60
```

## Example with the parallel environment (Slurm)

Likewise, if the `Slurm` (`sbatch` command) is available in your environment, you can add the `sbatch` command after the `--cluster` option.

**Note: To check if the command is executable, set smaller parameters such as rank_min=2 rank_max=2 trials=2 n_iter_max=2.**

```bash
snakemake -j 32 --config input=data/vaccine_tensor.npy outdir=output \
rank_min=1 rank_max=10 trials=50 n_iter_max=1000 ratio=30 \
--resources mem_gb=100 --use-singularity \
--cluster "sbatch -n 4 --nice=50 --requeue" --latency-wait 60
```

## Example with a local machine with Docker

If the `docker` command is available, the following command can be performed without installing any tools.

**Note: To check if the command is executable, set smaller parameters such as rank_min=2 rank_max=2 trials=2 n_iter_max=2.**

```bash
docker run --rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:main \
-i /work/data/vaccine_tensor.npy -o /work/output \
--cores=4 --rank_min=1 --rank_max=10 --trials=50 \
--n_iter_max=1000 --ratio=30 --memgb=10
```

## For Snakemake >=8 users
`--cluster CMD` option was removed from Snakemake v8.
Use `--executor cluster-generic --cluster-generic-submit-cmd CMD` instead.
To use this new feature, you have to install `snakemake-executor-plugin-cluster-generic` in advance.

cf.

https://stackoverflow.com/questions/77929511/how-to-run-snakemake-8-on-a-slurm-cluster
https://snakemake.readthedocs.io/en/latest/getting_started/migration.html#migrating-to-snakemake-8

# Reference
- [Ikeda K. et al., iScience, 2022](https://www.sciencedirect.com/science/article/pii/S2589004222015097)
- [TensorLy](http://tensorly.org/stable/index.html)

# Authors
- Koki Tsuyuzaki
- Eiryo Kawakami