FROM python:3.8-slim AS build
ENV PYTHONBUFFERED 1
RUN mkdir demo 
COPY . /demo
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN cd /demo
ENTRYPOINT ["python", "app.py"]