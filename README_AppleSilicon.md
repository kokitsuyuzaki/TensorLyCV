# Guideline for M1/M2 Mac users

This README is for M1/M2 Mac users.

In our environment, `Singularity` did not work properly for M1/M2 Mac (2022/1/6).

Therefore, the required tools for `TensorLyCV` are not available via the Docker container image file on M1/M2 Mac for now.

Instead, all required tools must be installed manually.

Here are the steps we followed on an M1 Mac.

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
mamba create -c conda-forge -c bioconda -c anaconda -n tensorlycv snakemake wget tensorly seaborn matplotlib -y
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

**Note that `--use-singularity` option does not work on M1/M2 Mac.**

```bash
snakemake -j 2 --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=30 \
--resources mem_gb=10
```

The meanings of all the arguments are below.

- `-j`: Snakemake option to set [the number of cores](https://snakemake.readthedocs.io/en/stable/executing/cli.html#useful-command-line-arguments) (e.g. 10, mandatory)
- `--config`: Snakemake option to set [the configuration](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html) (mandatory)
- `input`: Input file (e.g., vaccine_tensor.npy, mandatory)
- `outdir`: Output directory (e.g., output, mandatory)
- `rank`: Maximum rank parameter to search (e.g., the default value is 10, optional)
- `trials`: Number of random trials (e.g., the default value is 50, optional)
- `iters`: Number of iterations (e.g., the default value is 1000, optional)
- `ratio`: Sampling ratio of cross-validation (0 - 100, e.g., the default value is 20, optional)
- `--resources`: Snakemake option to control [resources](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#resources) (optional)
- `mem_gb`: Memory usage (GB, e.g. 10, optional)
- `--use-singularity`: Snakemake option to use Docker containers via [`Singularity`](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html) (mandatory)

## Example with a local machine with Docker

If the `docker` command is available, the following command can be performed without installing any tools.

**Note that `--platform linux/amd64` option is required on M1/M2 Mac.**

```bash
docker run --platform Linux/amd64 \
--rm -v $(pwd):/work ghcr.io/kokitsuyuzaki/tensorlycv:main \
-i /work/data/vaccine_tensor.npy -o /work/output \
--cores=2 --rank=2 --trials=2 --iters=2 \
--ratio=30 --memgb=100
```

# Authors
- Koki Tsuyuzaki
- Eiryo Kawakami