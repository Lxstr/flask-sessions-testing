# docker image
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ARG CACHEBUST=1
RUN groupadd -r app && useradd -r -g app app
RUN chsh -s /usr/sbin/nologin root
WORKDIR /app/
ADD ./requirements.txt /app/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt
USER app
ENV FLASK_DEBUG 0
ENV HOME /app