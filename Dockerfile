FROM python:3.7.0-slim-stretch
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/game-reviews-api/src
ADD src/requirements.txt /usr/src/game-reviews-api/src/
RUN pip install -r requirements.txt