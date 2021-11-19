ARG VERSION=stable-slim
FROM debian:${VERSION}

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt update && \
        apt install -y -q --no-install-recommends \
        gnuplot

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /plot

COPY redispipeline.dat .
COPY redispipeline.plt .

#build
CMD for i in *.plt; do gnuplot ${i}; BASENAME=$(basename $i .plt).jpg; echo ${BASENAME}; cp ${BASENAME} /output; done
