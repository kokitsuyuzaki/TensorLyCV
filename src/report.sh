# HTML
mkdir -p report
snakemake --report report/tensorlycv.html --config input=data/vaccine_tensor.npy outdir=output
