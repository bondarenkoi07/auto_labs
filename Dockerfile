FROM python:3.9-buster

RUN apt-get update && apt-get install conda
COPY . /app
RUN conda form --name auto_labs --file requirements.txt