FROM koki/tensorlycv_component:latest

ADD Snakefile /
ADD tensorlycv /
ADD src /src

WORKDIR /

ENTRYPOINT ["/tensorlycv"]
