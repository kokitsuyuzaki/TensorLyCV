FROM snakemake/snakemake:v7.18.2

ADD src /src
ADD Snakefile /
ADD tensorlycv /

RUN apt update && \
    apt install build-essential -y && \
    mamba install -c conda-forge numpy pandas tensorly matplotlib seaborn -y

WORKDIR /

ENTRYPOINT ["/tensorlycv"]
