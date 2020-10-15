FROM python:3.7-alpine
COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w 4", "server:app", "--bind", "0.0.0.0"]