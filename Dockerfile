FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app /app

CMD ["gunicorn", "-w 4", "server:app", "--bind", "0.0.0.0", "--reload"]