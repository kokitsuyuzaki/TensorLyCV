# Guideline for M1/M2 Mac users

This README is for M1/M2 Mac users.

In our environment, `Singularity` did not work properly on M1/M2 Mac (2023/1/6).

Therefore, for M1/M2 Mac user, the required tools for `TensorLyCV` are not available via the Docker container image file for now.

Instead, all required tools must be installed manually.

Here are the steps we followed on an M1 Mac to install the tools.

Note that this README is not exhaustive enough to solve all possible problems.

## Installation of all pre-requisites

First, we downloaded a shell script to install Mambaforge providing the minimum installer of `mamba` from the Miniforge website.
[https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-MacOSX-arm64.sh](https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-MacOSX-arm64.sh)

Then we performed the shell script as follows:

```bash
bash Mambaforge-MacOSX-arm64.sh
```

After rebooting the shell, we confirmed that the `mamba` command did work as follows:

```
exec $SHELL -l
mamba --version
```

Next, we created a `conda` environment containing the required tools in `TensorLyCV` as follows:

```bash
mamba create -c conda-forge -c bioconda -c anaconda -n tensorlycv snakemake wget tensorly=0.7.0 seaborn matplotlib -y
```

After activating the conda environment, we confirmed that the `snakemake` command did work as follows:

```bash
mamba activate tensorlycv
snakemake --version
```

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

**Note that `--use-singularity` option does not work on M1/M2 Mac.**

```bash
snakemake -j 4 --config input=data/vaccine_tensor.npy outdir=output \
rank_min=1 rank_max=10 trials=50 n_iter_max=1000 ratio=30 \
--resources mem_gb=10
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

## Example with a local machine with Docker

If the `docker` command is available, the following command can be performed without installing any tools.

**Note: To check if the command is executable, set smaller parameters such as rank_min=2 rank_max=2 trials=2 n_iter_max=2.**

**Note that `--platform linux/amd64` option is required on M1/M2 Mac.**

```bash
docker run --platform Linux/amd64 \
--rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:main \
-i /work/data/vaccine_tensor.npy -o /work/output \
--cores=4 --rank_min=1 --rank_max=10 --trials=50 \
--n_iter_max=1000 --ratio=30 --memgb=10
```

# Authors
- Koki Tsuyuzaki
- Eiryo Kawakami
