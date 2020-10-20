FROM python:3.7-alpine
COPY app /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w 1", "server:app", "--bind", "0.0.0.0", "--reload"]