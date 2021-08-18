

FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "src", "main.py" ]

# syntax=docker/dockerfile:1
# FROM python:3.6.9
# WORKDIR /code
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# EXPOSE 5000
# COPY . .
# CMD ["python", "./src/main.py"]