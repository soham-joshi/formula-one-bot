FROM python:3.8-slim AS build
ENV PYTHONBUFFERED 1
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]