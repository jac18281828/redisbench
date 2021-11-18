ARG VERSION=111021

FROM jac18281828/pythondev:${VERSION}

# build project
ARG PROJECT=push
WORKDIR /${PROJECT}

COPY requirements.txt .
COPY push.py .
COPY txndata.json .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -m compileall
ENV PYTHONPATH=.
CMD python3 push.py ${REDIS_SERVER} txndata.json
