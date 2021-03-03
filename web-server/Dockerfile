FROM python:3.6.10-buster

COPY . /app

RUN cd /app && pip3 install requirements.txt

WORKDIR /app

ENTRYPOINT ["python3", "app.py"]
