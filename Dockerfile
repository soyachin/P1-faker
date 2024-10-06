FROM python:3.8-slim

WORKDIR /mongo-faker

COPY . .

RUN pip3 install faker pydantic pymongo

CMD ["python3", "/mongo-faker/mongo.py"]
