FROM python:3

ARG http_proxy=http://wwwproxy.unimelb.edu.au:8000/
ARG https_proxy=http://wwwproxy.unimelb.edu.au:8000/
ARG no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au

ENV http_proxy=http://wwwproxy.unimelb.edu.au:8000/
ENV https_proxy=http://wwwproxy.unimelb.edu.au:8000/
ENV no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au

WORKDIR /harvester

RUN pip install --no-cache-dir tweepy couchdb

COPY . .

CMD [ "python", "./stream_harvester.py" ]