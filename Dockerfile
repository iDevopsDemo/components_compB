FROM python:3.8-alpine@sha256:3d93b1f77efce339aa77db726656872517b0d67837989aa7c4b35bd5ae7e81ba

LABEL maintainer="lars.gelbke@siemens.com"

ENV PYTHONPATH="/"

WORKDIR /

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./dataprovider /dataprovider/

CMD [ "python", "-m", "dataprovider.core" ]
