FROM python:3.6-alpine
MAINTAINER Isa Inalcik "info@software-testing.club"
RUN mkdir /app
COPY ./requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
