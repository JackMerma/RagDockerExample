FROM python:3.10-slim

WORKDIR /chatbot

COPY . /chatbot

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
