ARG VERSION=111021

FROM jac18281828/pythondev:${VERSION}

# build project
ARG PROJECT=rpop
WORKDIR /${PROJECT}

COPY requirements.txt .
COPY rpop.py .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -m compileall
ENV PYTHONPATH=.
CMD python3 rpop.py ${REDIS_SERVER} 
