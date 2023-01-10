# HTML
mkdir -p report
snakemake --report report/tensorlycv.html --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=20
