FROM python:3.6

# Do not buffer log messages in memory; some messages can be lost otherwise
ENV PYTHONUNBUFFERED 1

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /code

ADD . /code

ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
