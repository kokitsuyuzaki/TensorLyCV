# DAG graph
mkdir -p plot

snakemake --rulegraph \
--config input=data/vaccine_tensor.npy outdir=output \
rank=10 trials=50 iters=1000 ratio=30 | dot -Tpng > plot/dag.png