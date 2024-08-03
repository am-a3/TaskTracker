FROM python:3.10-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ /app/

EXPOSE 8000

EXPOSE 27017

ENV NAME=task-tracker-backend-docker
ENV DB_URL="mongodb://mongodb:27017/"

LABEL maintainer="sabreatom <aleksandrs.maklakovs@gmail.com>"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]DockerfileCopy code