FROM python:3.11-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9092

CMD ["gunicorn","-w","4","-b","0.0.0.0:9092","app:app"]

