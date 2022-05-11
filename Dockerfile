FROM python:3.8-slim AS build
WORKDIR /home
COPY . .
RUN ls /home
RUN echo $HOME
RUN pip install -r requirements.txt
CMD ["python3", "/home/app.py"]