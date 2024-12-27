FROM python:3.6

# Do not buffer log messages in memory; some messages can be lost otherwise
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD . /code

ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
