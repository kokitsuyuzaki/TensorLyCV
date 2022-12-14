FROM koki/tensorlycv_component:latest

ADD src /src
ADD tensorlycv /
ADD Snakefile /

WORKDIR /

ENTRYPOINT ["/tensorlycv"]
