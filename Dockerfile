FROM python:3.8-slim AS build
WORKDIR /demo
ENV PYTHONBUFFERED 1
COPY . .
RUN ls /demo
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./app.py"]