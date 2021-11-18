FROM python:latest
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip
RUN mkdir -p /code/

WORKDIR /code/
COPY ./requirements.txt .

RUN python -m pip install -r requirements.txt
COPY . /code/
