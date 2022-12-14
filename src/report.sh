# HTML
mkdir -p report

snakemake --report report/tensorlycv.html \
--config input=data/vaccine_tensor.npy outdir=output \
rank=10 trials=50 iters=1000 ratio=30