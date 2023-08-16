FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEPLOY_RUN = True

RUN apt-get update && apt-get -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim \
    && apt-get install -y postgresql-client build-essential libpq-dev

COPY requirements.txt /temp/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password root-user

COPY ./src ./src
WORKDIR /src

RUN chown -R root-user:root-user /src/

USER root-user

CMD gunicorn -w 3 --chdir ./src config.wsgi --bind 0.0.0.0:8000 --forwarded-allow-ips=*.*
