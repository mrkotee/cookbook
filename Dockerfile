FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt update && apt upgrade -y && apt install -y netcat
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt


RUN mkdir /cookbook
COPY ./cookbook /cookbook
WORKDIR /cookbook

COPY entrypoint.sh .

ENTRYPOINT ["/cookbook/entrypoint.sh"]
