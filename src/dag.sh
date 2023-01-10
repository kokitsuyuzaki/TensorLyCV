# DAG graph
mkdir -p plot
snakemake --rulegraph --config input=data/vaccine_tensor.npy outdir=output \
rank=2 trials=2 iters=2 ratio=30 | dot -Tpng > plot/dag.png
