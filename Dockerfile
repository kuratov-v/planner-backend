FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update 
RUN apt-get install -y netcat
RUN mkdir /app

ADD requirements.txt /app/
RUN pip install -r app/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
