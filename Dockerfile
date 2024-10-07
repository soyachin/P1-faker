FROM python:3.8-slim

WORKDIR /app

COPY myseq.py .
COPY .env .

RUN pip3 install --no-cache-dir python-dotenv psycopg2-binary mysql-connector-python pymongo faker

CMD ["python3", "myseq.py"]