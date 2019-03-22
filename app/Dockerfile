FROM python:3
RUN apt-get -qq -y update \
    && apt-get -qq -y clean all \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
# collect static files
RUN ./manage.py collectstatic --noinput --clear
