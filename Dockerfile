FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /app

ADD requirements.txt /app/
RUN pip install -r app/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000