FROM python:3.9-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ /app/

EXPOSE 80

ENV NAME=task-tracker-backend-docker

LABEL maintainer="sabreatom <aleksandrs.maklakovs@gmail.com>"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]DockerfileCopy code