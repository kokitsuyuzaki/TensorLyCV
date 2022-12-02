FROM snakemake/snakemake:v7.18.2

ADD src /src
ADD Snakefile /
ADD tensorlycv /

WORKDIR /

ENTRYPOINT ["/tensorlycv"]
