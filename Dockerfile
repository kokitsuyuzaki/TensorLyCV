FROM koki/tensorlycv_component:latest

ADD src /src
ADD Snakefile /
ADD tensorlycv /

WORKDIR /

ENTRYPOINT ["/tensorlycv"]
