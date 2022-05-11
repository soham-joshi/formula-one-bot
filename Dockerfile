FROM python:3.8-slim AS build
WORKDIR /home
ENV PYTHONBUFFERED 1
COPY . .
RUN ls /home
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "./app.py"]