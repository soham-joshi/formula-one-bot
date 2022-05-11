FROM alpine:latest
WORKDIR /home
COPY . .
RUN ls /home
RUN echo $HOME
RUN pip install -r requirements.txt
CMD ["python", "/home/app.py"]