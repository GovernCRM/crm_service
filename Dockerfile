FROM python:3.11

# Do not buffer log messages in memory; some messages can be lost otherwise
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY /requirements.txt /requirements.txt

WORKDIR /code

RUN apt update \
    && apt -y upgrade \
    && apt install -y python3 python3-pip poppler-utils libsm6 libxext6 libxrender-dev postgresql netcat-traditional

# Install the project requirements.
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt --no-cache-dir

ADD . /code

# Collecting static files
RUN ./scripts/run-collectstatic.sh

EXPOSE 8080
ENTRYPOINT ["bash", "/code/scripts/docker-entrypoint.sh"]

# Specify tag name to be created on github
LABEL version="1.0.0"