# DAG graph
mkdir -p plot
snakemake --rulegraph --config input=data/vaccine_tensor.npy outdir=output | dot -Tpng > plot/dag.png
