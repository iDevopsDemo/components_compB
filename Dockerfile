FROM docker.artifactory.mydevops.info/python:3.8-alpine

LABEL maintainer="lars.gelbke@siemens.com"

ENV PYTHONPATH="/"

WORKDIR /

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./datacollector /datacollector/

CMD [ "python", "-m", "datacollector.core" ]
