# HTML
mkdir -p report
snakemake --report report/tensorlycv.html \
--config input=data/vaccine_tensor.npy outdir=output \
rank_min=2 rank_max=3 \
trials=2 n_iter_max=2
