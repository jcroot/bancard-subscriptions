FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y libssl-dev python3-mysqldb
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
