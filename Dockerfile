FROM python:3.12

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y postgresql-client

RUN chmod +x ./wait-for-postgres.sh

RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]