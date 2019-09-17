FROM python:3.7.4

WORKDIR /vegetables/

ADD . .

RUN pip install -r requirements.txt
