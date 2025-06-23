FROM python:3.12-bookworm

RUN apt-get update && apt-get install -y git sed

WORKDIR /cleanvul_test

RUN git clone https://github.com/yikun-li/CleanVul.git && \
    cp -r CleanVul/datasets . && \
    ls -la datasets/

ENV CLEANVUL_DATASETS=/cleanvul_test/datasets

RUN pip install pandas numpy