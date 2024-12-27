FROM --platform=linux/amd64 python:3.7-alpine3.10

# Do not buffer log messages in memory; some messages can be lost otherwise
ENV PYTHONUNBUFFERED 1

RUN apk update

# Install the project requirements.
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

WORKDIR /code

ADD . /code

ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
