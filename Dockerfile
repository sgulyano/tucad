# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6-alpine
LABEL maintainer="y_sarun@hotmail.com"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /tucad

# Set the working directory to /music_service
WORKDIR /tucad

# Copy the current directory contents into the container at /music_service
COPY . /tucad/

# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev \
  # && pip install psycopg2

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install psycopg2 \
  && apk del build-deps

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


CMD python manage.py runserver 0.0.0.0:8000