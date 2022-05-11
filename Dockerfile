FROM python:3.8-slim AS build
WORKDIR /demo
ENV PYTHONBUFFERED 1
RUN mkdir src 
COPY . ./src
RUN ls /demo
RUN pip install -r ./src/requirements.txt
ENTRYPOINT ["python", "./src/app.py"]