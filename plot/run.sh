#!/usr/bin/env bash

VERSION=$(date +%m%d%y)

OUTDIR=$(pwd)/output

if [ ! -d ${OUTDIR} ]
then
    mkdir -p ${OUTDIR}
fi    

docker build . -t searchplt:${VERSION} && \
	docker run -v ${OUTDIR}:/output --rm -i -t searchplt:${VERSION}
