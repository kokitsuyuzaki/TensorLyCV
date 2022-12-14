FROM koki/tensorlycv_component:latest

ADD tensorlycv /
ADD src /src
ADD Snakefile /

WORKDIR /

ENTRYPOINT ["/tensorlycv"]
