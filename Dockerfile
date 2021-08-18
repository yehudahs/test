# syntax=docker/dockerfile:1
FROM python:3.6.9
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "./src/main.py"]