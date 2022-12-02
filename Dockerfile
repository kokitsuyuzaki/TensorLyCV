FROM snakemake/snakemake:v7.18.2

ADD src /
ADD Snakefile /

ENTRYPOINT ["src/entrypoint.sh"]
