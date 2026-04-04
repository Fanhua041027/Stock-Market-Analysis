FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x init.sh train.sh test.sh

CMD ["bash", "init.sh"]